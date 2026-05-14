from typing import Dict


class ZeltaKellyAllocator:
    """
    Determines exactly how much capital to deploy (in NGN)
    using a SAFE Half-Kelly system + behavioral constraints.

    This is NOT just profit maximization — it is capital protection first.

    Output integrates directly into brain/pipeline.py.
    """

    KELLY_MULTIPLIER = 0.50
    MAX_ALLOCATION_PCT = 0.15
    MIN_AMOUNT_NGN = 500.0
    DEFAULT_PAYOFF_RATIO = 1.5

    # ─────────────────────────────────────────────────────────────

    def calculate_base_kelly(
        self,
        win_probability: float,
        payoff_ratio: float = None,
    ) -> float:

        payoff_ratio = payoff_ratio or self.DEFAULT_PAYOFF_RATIO
        loss_probability = 1.0 - win_probability

        kelly_pct = win_probability - (loss_probability / payoff_ratio)

        return max(0.0, kelly_pct)

    # ─────────────────────────────────────────────────────────────

    def scale_by_confidence(
        self,
        base_allocation: float,
        confidence_score: int,
    ) -> float:

        return base_allocation * (confidence_score / 100.0)

    # ─────────────────────────────────────────────────────────────

    def apply_stress_cap(
        self,
        allocation_pct: float,
        stress_score: int,
    ) -> float:

        if stress_score >= 80:
            return min(allocation_pct, 0.05)

        elif stress_score >= 60:
            return min(allocation_pct, 0.10)

        return min(allocation_pct, self.MAX_ALLOCATION_PCT)

    # ─────────────────────────────────────────────────────────────

    def calculate_invest_amount(
        self,
        free_cash: float,
        win_probability: float,
        confidence_score: int,
        stress_score: int,
    ) -> float:

        base_kelly = self.calculate_base_kelly(win_probability)

        if base_kelly <= 0:
            return 0.0

        fractional_kelly = base_kelly * self.KELLY_MULTIPLIER

        confidence_adjusted = self.scale_by_confidence(
            fractional_kelly,
            confidence_score
        )

        final_pct = self.apply_stress_cap(
            confidence_adjusted,
            stress_score
        )

        raw_amount = free_cash * final_pct

        if raw_amount < self.MIN_AMOUNT_NGN:
            return 0.0

        return round(raw_amount, 2)

    # ─────────────────────────────────────────────────────────────

    def calculate_save_amount(
        self,
        free_cash: float,
        stress_score: int,
    ) -> float:

        if stress_score >= 80:
            pct = 0.60
        elif stress_score >= 60:
            pct = 0.40
        elif stress_score >= 30:
            pct = 0.25
        else:
            pct = 0.15

        amount = free_cash * pct

        if amount < self.MIN_AMOUNT_NGN:
            return 0.0

        return round(amount, 2)

    # ─────────────────────────────────────────────────────────────

    def run(
        self,
        bayesian_data: Dict,
        confidence_data: Dict,
        wallet_data: Dict,
    ) -> Dict:

        verdict          = bayesian_data.get("verdict", "HOLD")
        win_probability  = bayesian_data.get("win_probability", 0.5)
        stress_score     = bayesian_data.get("stress_score", 50)

        is_actionable    = confidence_data.get("is_actionable", False)
        confidence_score = confidence_data.get("confidence_score_100", 0)

        free_cash     = wallet_data.get("free_cash", 0.0)
        total_balance = wallet_data.get("total_balance", free_cash)

        # Fix 4: survival_mode / emergency_mode guard from student_model
        student_model  = wallet_data.get("student_model", {})
        agent_mode     = student_model.get("agent_mode", "NORMAL")
        emergency_mode = student_model.get("emergency_mode", False)
        survival_mode  = student_model.get("survival_mode", False)
        weeks_runway   = student_model.get("weeks_of_runway", 30)

        # EMERGENCY: hard block — hold everything, no allocation
        if emergency_mode or agent_mode == "EMERGENCY":
            return self._response(
                "HOLD", 0, 0, free_cash, 0,
                f"⚠️ EMERGENCY: Money runs out in {weeks_runway:.1f} weeks. "
                "Hold all funds. Cut non-essential spending immediately."
            )

        # SURVIVAL: force protect mode — no discretionary spending allowed
        if survival_mode or agent_mode == "SURVIVAL":
            save_amount = self.calculate_save_amount(free_cash, max(int(stress_score), 70))
            hold_amount = max(0.0, free_cash - save_amount)
            pct = round((save_amount / free_cash) * 100, 1) if free_cash > 0 else 0
            return self._response(
                "SAVE", 0, save_amount, hold_amount, pct,
                f"SURVIVAL mode. Protect ₦{save_amount:,.0f}. "
                f"Keep ₦{hold_amount:,.0f} for essentials only."
            )

        # ── HARD SAFETY LAYER ─────────────────────────────────────

        if free_cash <= 0:
            return self._response("HOLD", 0, 0, 0, 0, "No free cash available.")

        if not is_actionable:
            return self._response(
                "HOLD",
                0,
                0,
                free_cash,
                0,
                "Signal not strong enough. Capital protected."
            )

        # ── INVEST ───────────────────────────────────────────────

        if verdict == "INVEST":

            invest_ngn = self.calculate_invest_amount(
                free_cash,
                win_probability,
                confidence_score,
                stress_score
            )

            if invest_ngn == 0:
                return self._response(
                    "HOLD",
                    0,
                    0,
                    free_cash,
                    0,
                    "Kelly size too small. Skipping trade."
                )

            remaining = free_cash - invest_ngn

            save_ngn = round(remaining * 0.30, 2)
            hold_ngn = round(remaining - save_ngn, 2)

            pct = round((invest_ngn / free_cash) * 100, 1)

            notes = (
                f"Kelly={round(self.calculate_base_kelly(win_probability)*100,1)}% | "
                f"Confidence={confidence_score} | Stress={stress_score} → "
                f"{pct}% allocation"
            )

            return self._response(
                "INVEST",
                invest_ngn,
                save_ngn,
                hold_ngn,
                pct,
                notes
            )

        # ── SAVE ────────────────────────────────────────────────

        elif verdict == "SAVE":

            save_ngn = self.calculate_save_amount(
                free_cash,
                stress_score
            )

            hold_ngn = round(free_cash - save_ngn, 2)

            pct = round((save_ngn / free_cash) * 100, 1)

            return self._response(
                "SAVE",
                0,
                save_ngn,
                hold_ngn,
                pct,
                f"Stress-driven capital protection ({stress_score})"
            )

        # ── HOLD ────────────────────────────────────────────────

        return self._response(
            "HOLD",
            0,
            0,
            free_cash,
            0,
            "No strong edge detected."
        )

    # ─────────────────────────────────────────────────────────────

    def _response(
        self,
        verdict: str,
        invest: float,
        save: float,
        hold: float,
        pct: float,
        notes: str,
    ) -> Dict:

        return {
            "verdict": verdict,
            "invest_ngn": invest,
            "save_ngn": save,
            "hold_ngn": hold,
            "allocation_pct": pct,
            "allocator_notes": notes,
            "plain_english": self._explain(verdict, invest, save, hold),
        }

    # ─────────────────────────────────────────────────────────────

    def _explain(
        self,
        verdict: str,
        invest: float,
        save: float,
        hold: float,
    ) -> str:

        if verdict == "INVEST":
            return (
                f"Invest ₦{invest:,.0f}. Save ₦{save:,.0f}. "
                f"Hold ₦{hold:,.0f}. Controlled risk using Kelly sizing."
            )

        if verdict == "SAVE":
            return (
                f"Save ₦{save:,.0f}. Hold ₦{hold:,.0f}. "
                f"Market risk is elevated."
            )

        return (
            f"Hold ₦{hold:,.0f}. No strong opportunity right now."
        )


# ── PIPELINE ENTRY POINT ────────────────────────────────────────

def run_kelly_allocator(
    bayesian_data: Dict,
    confidence_data: Dict,
    wallet_data: Dict,
) -> Dict:

    allocator = ZeltaKellyAllocator()
    result = allocator.run(
        bayesian_data,
        confidence_data,
        wallet_data
    )

    print(
        f"[QUELO Kelly] {result['verdict']} | "
        f"₦{result['invest_ngn']:,.0f} invest"
    )

    return result