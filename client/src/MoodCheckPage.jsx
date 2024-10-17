import React, { useEffect } from "react";
import { useOutletContext, useNavigate } from "react-router-dom";

const MoodCheckPage = () => {

  const navigate = useNavigate();

  const { mood, setMood } = useOutletContext();
  const handleMood = (event) => {
    setMood(event.target.alt);
  };

  const handleClick = () => {
    navigate("/element_select");
  }

  useEffect(() => {
    console.log(mood);
  }, [mood]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-6">
      <h1 className="text-3xl font-bold text-center">How do you feel today?</h1>
      <div className="flex gap-3">
        <img
          src="/emoji_face_angry.png"
          alt="angry"
          className="w-36 hover:bg-base-200 cursor-pointer"
          onClick={handleMood}
        />
        <img
          src="/emoji_face_happy.png"
          alt="happy"
          className="w-36 hover:bg-base-200 cursor-pointer"
          onClick={handleMood}
        />
        <img
          src="/emoji_face_savoring_food.png"
          alt="savoring food"
          className="w-36 hover:bg-base-200 cursor-pointer"
          onClick={handleMood}
        />
        <img
          src="/emoji_weary_face.png"
          alt="weary"
          className="w-36 hover:bg-base-200 cursor-pointer"
          onClick={handleMood}
        />
      </div>
      <button className='btn btn-primary' onClick={handleClick}>Next</button>

    </div>
  );
};

export default MoodCheckPage;
