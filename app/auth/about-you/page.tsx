"use client";

import { useState } from "react";
import {
  ArrowRight,
  ArrowLeft,
  Check,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useRouter } from "next/navigation";

const steps = [
  {
    id: 1,
    questions: [
      {
        label: "How often do you receive money?",
        options: [
          "Weekly",
          "Monthly",
          "Randomly",
          "Daily",
        ],
      },
      {
        label: "Average weekly allowance?",
        options: [
          "₦0 - ₦10k",
          "₦10k - ₦30k",
          "₦30k - ₦70k",
          "₦70k+",
        ],
      },
    ],
  },

  {
    id: 2,
    questions: [
      {
        label: "What do you spend most on?",
        options: [
          "Food",
          "Transport",
          "Shopping",
          "Data",
          "Entertainment",
        ],
      },

      {
        label: "When money finishes, what do you do?",
        options: [
          "Borrow",
          "Reduce spending",
          "Find gigs",
          "Ask family/friends",
        ],
      },
    ],
  },

  {
    id: 3,
    questions: [
      {
        label: "How do you spend generally?",
        options: [
          "Careful",
          "Balanced",
          "Impulsive",
        ],
      },

      {
        label: "Your risk preference?",
        options: [
          "Low Risk",
          "Moderate",
          "High Risk",
        ],
      },
    ],
  },

  {
    id: 4,
    questions: [
      {
        label: "Primary goal?",
        options: [
          "Save Money",
          "Track Spending",
          "Avoid Bad Decisions",
          "Find Gigs",
          "Survive Longer",
        ],
      },
    ],
  },
];

export default function AboutYou() {
  const router = useRouter();

  const [currentStep, setCurrentStep] = useState(0);

  const [answers, setAnswers] = useState<
    Record<string, string>
  >({});

  const current = steps[currentStep];

  const handleSelect = (
    question: string,
    option: string
  ) => {
    setAnswers((prev) => {
      const alreadySelected =
        prev[question] === option;

      if (alreadySelected) {
        const updated = { ...prev };
        delete updated[question];
        return updated;
      }

      return {
        ...prev,
        [question]: option,
      };
    });
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const allAnswered = current.questions.every(
    (q) => answers[q.label]
  );

  return (
    <div className="min-h-screen flex">
    <div className="flex items-center justify-center px-2.5 py-10 relative overflow-hidden w-full">

      <div className="relative z-10 w-full max-w-xl">

        {/* Header */}
        <div className="mb-6">

          <div className="mb-6 relative">
            <h1 className=" text-2xl font-bold  tracking-wider  mb-3 text-[#090536]">Tell Zelta about yourself.</h1>
            <p className="text-neutral-600 text-sm">It helps Zelta understand more about you.</p>
          </div>

          <div className="flex items-center max-w-[150px] justify-end gap-3 mb-5">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`h-1 flex-1 rounded-full transition-all duration-500 ${
                  index <= currentStep
                    ? "bg-black"
                    : "bg-neutral-300"
                }`}
              />
            ))}
          </div>

          <div className="flex items-center justify-between">

            <div>
              <p className="text-sm text-neutral-500 mb-2">
                STEP {currentStep + 1}
              </p>
            </div>


          </div>
        </div>

        {/* Main Card */}
        <div className="">

          <div className="space-y-6">
            {current.questions.map((question) => (
              <div key={question.label}>

                <h2 className="text-[16px] font-semibold mb-5">
                  {question.label}
                </h2>

                <div className="grid grid-cols-2 gap-4">

                  {question.options.map((option) => {
                    const selected =
                      answers[question.label] === option;

                    return (
                      <button
                        key={option}
                        onClick={() =>
                          handleSelect(
                            question.label,
                            option
                          )
                        }
                        className={`group px-4 py-2 rounded-md lg:rounded-xl border transition-all duration-300 text-left cursor-pointer
                          
                          ${
                            selected
                              ? " bg-[#090536] text-white shadow-lg scale-0.4]"
                              : "border-neutral-200 bg-white "
                          }
                        `}
                      >
                        <div className="flex items-center justify-between">

                          <span className="text-sm">
                            {option}
                          </span>

                          <div
                            className={`w-4 h-4 rounded-full border flex items-center justify-center transition-all
                              
                              ${
                                selected
                                  ? "border-white bg-white text-black"
                                  : "border-neutral-300"
                              }
                            `}
                          >
                            {selected && (
                              <Check size={14} />
                            )}
                          </div>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Footer Buttons */}
          <div className="flex items-center justify-between mt-14">

            <button
              onClick={prevStep}
              disabled={currentStep === 0}
              className="flex items-center gap-2 text-sm font-bold cursor-pointer"
            >
              <ChevronLeft size={16} />
              Back
            </button>

            {currentStep === steps.length - 1 ? (
              <button
                onClick={() =>
                  router.push("/dashboard")
                }
                disabled={!allAnswered}
                className="bg-[#090536] text-white px-7 py-3 rounded-2xl  transition-all hover:scale-[1.03] disabled:opacity-50 disabled:hover:scale-100 text-sm font-bold cursor-pointer"
              >
                Continue to Dashboard
              </button>
            ) : (
              <button
                onClick={nextStep}
                disabled={!allAnswered}
                className="bg-[#090536] font-bold text-white px-7 py-2 rounded-3xl text-sm flex items-center gap-2 transition-all hover:scale-[1.03] cursor-pointer "
              >
                Continue
                <ChevronRight size={18} />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}