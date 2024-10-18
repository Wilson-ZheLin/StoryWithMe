import React, { useEffect, useState} from 'react'
import {ReactComponent as Logo} from './logo.svg'
import { useNavigate, useParams } from 'react-router-dom'


const StoryDetailPage = () => {
  const { pageId } = useParams();
  const navigate = useNavigate(); 

  const [story, setStory] = useState('');
  const [currentPage, setCurrentPage] = useState(parseInt(pageId, 10));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getStory = () => {    
    setLoading(true);
    fetch('/get_story', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    }).then(res => res.json())
    .then(story => {
      setStory(story);
      console.log(story);
      setLoading(false);
    })
    .catch(error=>{
      console.log(error);
      setError('Error fetching story json');
      setLoading(false);
    })
  }

  useEffect(() => {
    getStory();
  }, [currentPage])

  const handleNextPage = () => {
    const nextPageId = currentPage + 1;;
    if (nextPageId > story.pages) {
      navigate('/story_gallery');
    } else {
      setCurrentPage(nextPageId);
      navigate(`/story/${nextPageId}`);
    }
  };

  const handlePreviousPage = () => {
    const prevPageId = currentPage - 1
    if (prevPageId < 1) {
      return;
    } else {
      setCurrentPage(prevPageId);
      navigate(`/story/${prevPageId}`);
    }
  };


  return (
    <>
      <div className='flex flex-col items-center justify-start min-h-screen gap-4'>
        <div className='h-40 w-full'>
          <Logo className='h-full w-full'/>
        </div>

        <ul className="steps">
          <li data-content="" className="step step-primary"></li>
          <li data-content="" className="step"></li>
          <li data-content="★" className="step"></li>
          <li data-content="" className="step"></li>
          <li data-content=""className="step"></li>
          <li data-content="●" className="step"></li>
        </ul>

        <h1 className='text-2xl font-bold text-center'>{story.title}</h1>
        <div className="flex items-center justify-center gap-8">
          <button disabled={currentPage === 1} onClick={handlePreviousPage}>
            <img 
              src="/left.png" 
              className={`w-20  ${currentPage === 1 ? 'opacity-20 cursor-not-allowed' : 'cursor-pointer hover:bg-base-200'}`} 
              alt="previous page"></img>
          </button>
          <img src="https://placehold.co/1000x500"></img>
          <button onClick={handleNextPage}>
            <img 
              src="/next.png" 
              className='w-20 hover:bg-base-200 cursor-pointer' 
              alt="next page"></img>
          </button>
        </div>
        <div>
          {loading && <span className="loading loading-dots loading-sm"></span>}
          {error && <p>{error}</p>}
          {story && (
          <div className="max-w-7xl flex flex-col items-center justify-center gap-6">
              <p>{story.parts[currentPage - 1]}</p>
          </div>
        )}
        </div>
      </div>
    </>
  )
}

export default StoryDetailPage