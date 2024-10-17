import React, { useState, useEffect }  from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'

const GenerateStoryPage = () => {
  const navigate = useNavigate(); 

  const {name, age, readTime, hobbies, elements, mood} = useOutletContext()

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
      body: JSON.stringify({ age, readTime, elements }) // TODO:add hobbies as a parameter, need to modify the prompt
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
      <h1 className='text-3xl font-bold pt-12 text-center'>Generating the story...</h1>
          {loading && <span className="loading loading-dots loading-sm"></span>}
          {error && <p>{error}</p>}
          {data && (
          <div className="max-w-7xl flex flex-col items-center justify-center gap-6">
              <p>{data.story}</p>
              <button className='btn btn-primary' onClick={()=>navigate('/story/1')}>All set, let's go!</button>
          </div>
          )}
    </div>
  )
}

export default GenerateStoryPage

