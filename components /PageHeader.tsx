import React from "react";
// import PagesHeading from "./PagesHeading";

interface PageHeaderProps {
  title: string;
  description: string;
}

function PageHeader({ title, description }: PageHeaderProps) {
  return (
    <div>
      <h2 className="text-[20px] lg:text-[24px] font-bold md:text-3xl">
        {title}
      </h2>
      <p className="text-gray-600 text-[15px] lg:text-[18px] md:text-lg">
        {description}
      </p>
    </div>
  );
}

export default PageHeader;
