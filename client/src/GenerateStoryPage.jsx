import React, { useState, useEffect, useRef }  from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'
import Confetti from 'react-confetti'
// import useWindowSize from 'react-use/lib/useWindowSize'


const GenerateStoryPage = () => {

  const navigate = useNavigate(); 
  const {name, age, readTime, hobbies, elements, mood, voiceCharacter, voiceCharacterPath} = useOutletContext()


  const [data, setData] = useState({})
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Send data to server to generate story
  const generateStory = () => {
    setLoading(true);
    fetch('/generate_story', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ age, readTime, elements, mood, hobbies, voiceCharacter, voiceCharacterPath }) 
    })
      .then(res => res.json())
      .then(data => {
        setData(data);
        console.log(data); // For testing
        setLoading(false);
      })
      .catch(error => {
        console.log(error);
        setError('Error fetching data');
        setLoading(false);
      });
  };

  useEffect(()=>{
    generateStory()
  }, [])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-6">
          {loading && 
            <div className='flex flex-col items-center justify-center'>
              <h1 className='text-3xl font-bold pt-12 text-center'>Creating the story...</h1>
              <img src="/loading_animation.gif" className="w-80 h-auto" alt="loading" />          
              {/* <span className="loading loading-dots loading-sm"></span> */}
            </div>
          }
          {error && 
            <p>{error}</p>
          }
          {!loading && data && (
            <div className="max-w-7xl flex flex-col items-center justify-center gap-6">
                {/* <p>{data.story}</p> */}
                <Confetti />
                <button className='btn btn-primary btn-lg btn-wide' onClick={()=>navigate('/story/1')}>All set, let's go!</button>
            </div>
          )}
    </div>
  )
}

export default GenerateStoryPage

