import React, { useEffect, useState} from 'react'
import {ReactComponent as Logo} from './logo.svg'
import { useNavigate } from 'react-router-dom'


const StoryDetailPage = () => {

  const navigate = useNavigate(); 

  const [currentPage, setCurrentPage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getStoryCurrentPage = () => {

    // TODO: change the endpoint to '/current_page'
    
    setLoading(true);
    fetch('/next_page', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    }).then(res => res.json())
    .then(currentPage => {
      setCurrentPage(currentPage);
      console.log(currentPage);
      setLoading(false);
    })
    .catch(error=>{
      console.log(error);
      setError('Error fetching current page');
      setLoading(false);
    })
  }

  useEffect(() => {
    getStoryCurrentPage();
  }, [])


  return (
    <>
      <div className='flex flex-col items-center justify-start min-h-screen gap-4'>
        <div className='h-40 w-full'>
          <Logo className='h-full w-full'/>
        </div>
        <h1 className='text-2xl font-bold text-center'>Story Title</h1>
        <div className="flex items-center justify-center gap-8">
          <img src="/left.png" className='w-20 hover:bg-base-200 cursor-pointer'></img>
          <img src="https://placehold.co/1000x500"></img>
          <img src="/next.png" className='w-20 hover:bg-base-200 cursor-pointer' onClick={()=>navigate('/story/2')}></img>
        </div>
        <div>
          {loading && <span className="loading loading-dots loading-sm"></span>}
          {error && <p>{error}</p>}
          {currentPage && (
          <div className="max-w-7xl flex flex-col items-center justify-center gap-6">
              <p>{currentPage.story}</p>
          </div>
        )}
        </div>
      </div>
    </>
  )
}

export default StoryDetailPage