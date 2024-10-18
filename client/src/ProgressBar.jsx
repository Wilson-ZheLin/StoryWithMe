import React from 'react'

const ProgressBar = ({pages, currentPage}) => {

    // create an array of pages and map over to create a list of steps
    const listItems = Array(pages).fill().map((_, index) => {
        let dataContent = "";
        if (index === pages - 1) {
            dataContent = "●";
        } else if (index === 2) {
            dataContent = "★";
        } else {
            dataContent = "";
        }

        const className = `step ${index <= currentPage - 1 ? 'step-primary' : ''}`;

        return (
          <li key={index} data-content={dataContent} className={className}></li>
        );
      });

  return (
    <>
        <ul className="steps">
            {listItems}
        </ul>  
    </>
  )
}

export default ProgressBar