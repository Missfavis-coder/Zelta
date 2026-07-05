

const sections = [
    {
      title: "Information we collect",
      body: `To provide ZELTA's services, we collect information you choose to share with us, such as your name, email address, school, account details, spending plans, transaction history, and financial preferences. `
    },
    {
      title: "How we use your information",
      body: `Your information helps us personalize your experience, monitor spending habits, generate AI-powered financial insights, recommend budgets, notify you before overspending, suggest relevant student gigs when necessary, improve our services, and protect against fraud or unauthorized activity.`,
    },
    {
      title: "Your data belongs to you",
      body: `Your personal information remains yours. We do not sell your personal data to advertisers or unrelated third parties. Information is only shared with carefully selected service providers when necessary to deliver ZELTA's services securely.`,
    },
    {
      title: "Keeping your money secure",
      body: `Payments and financial data are protected using industry-standard encryption and secure banking infrastructure. Sensitive information is encrypted both during transmission and while stored.`,
    },
    {
      title: "Trusted partners",
      body: `We work with trusted infrastructure providers for authentication, cloud hosting, payment processing, analytics, and fraud prevention. These partners are required to protect your information and only process it on our behalf.`,
    },
    {
      title: "Your choices",
      body: `You can review or update your account information, request deletion of your account where applicable, manage notification preferences, and contact us if you have questions about your privacy or how your information is handled.`,
    },
    {
      title: "Need help?",
      body: `If you have any questions, concerns, or wish to report a security issue, our support team is available to help. We'll respond as quickly as possible and work with you to resolve any issues.`,
    },
  ];
export default function PrivacyPage() {
  return (
    <main className="min-h-screen ">
      <div className="mx-auto max-w-5xl px-6 py-24 mt-18">

        {/* Header */}

        <div className="max-w-3xl mx-auto text-center">
          <span className="text-xs uppercase tracking-[0.25em] text-amber-500">
            Privacy
          </span>

          <h1 className="text-xl lg:text-3xl md:text-3xl text-white dark:text-[#160a2a]/90 text-center font-bold tracking-tight my-2 ">
            Privacy first.
            <br />
            Security by default.
          </h1>

          <p className="mt-5 md:text-[15px] text-sm leading-7 text-gray-300 dark:text-foreground/80">
            Every decision we make starts with protecting your personal
            information, your finances and your trust.
          </p>
        </div>



        {/* Sections */}

        <div className="space-y-14 mt-18">
          {sections.map((section) => (
            <section
              key={section.title}
              className="grid md:grid-cols-12 gap-8 border-b border-neutral-800 dark:border-neutral-200 pb-14"
            >
              <div className="md:col-span-4">
                <h2 className="md:text-lg text-[16px] font-semibold dark:text-[#160a2a]/90 text-white">
                  {section.title}
                </h2>
              </div>

              <div className="md:col-span-8">
                <p className="max-w-xl text-sm leading-7 text-gray-300 dark:text-foreground/70">
                  {section.body}
                </p>
              </div>
            </section>
          ))}
        </div>

        {/* Bottom */}

        <div className="mt-20 flex flex-wrap gap-8 text-sm text-neutral-400 dark:text-foreground/90">

          <span>256-bit encryption</span>

          <span>Trusted payment partners</span>

          <span>Secure authentication</span>

          <span>Fraud monitoring</span>

          <span>24/7 support</span>

        </div>

      </div>
    </main>
  );
}