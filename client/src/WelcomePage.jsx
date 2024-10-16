import React from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'

const WelcomePage = () => {
  const navigate = useNavigate(); 

  const { name } = useOutletContext();

  const handleStart = () => {
    navigate('/mood_check')
  }

  return (
    <div className='flex flex-col items-center justify-center min-h-screen gap-6'>
        <h1 className='text-3xl font-bold text-center'>Hello, {name}</h1>
        <h2 className='text-xl font-bold text-center'>Welcome to StoryWithMe!</h2>
        <button className="btn btn-primary" onClick={handleStart}>Started</button>
    </div>
  )
}

export default WelcomePage