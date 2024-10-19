import React from "react";

const InteractionWindow = () => {
  return (
    <div className="flex justify-between" >
      {/* voic character */}
      <div className="chat chat-start">
        <div className="chat-image avatar">
          <div className="w-10 rounded-full">
            <img
              alt="Tailwind CSS chat bubble component"
              src="/olive.svg"
            />
          </div>
        </div>
        <div className="chat-header">
          Olive
        </div>
        <div className="chat-bubble">Prompt a question based on the current story progress.</div>
      </div>

      {/* kid's response */}
      <div className="chat chat-end">
        <button className="btn btn-circle">
          <img src="/speak.svg" alt="speakIcon" />
        </button>
        {/* <div className="chat-bubble"></div> */}
      </div>
    </div>
  );
};

export default InteractionWindow;
