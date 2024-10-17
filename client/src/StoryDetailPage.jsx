import React from 'react'
import {ReactComponent as Logo} from './logo.svg'


const StoryDetailPage = () => {
  return (
    <>
      <div className='flex flex-col items-center justify-start min-h-screen gap-4'>
        <div className='h-40 w-full'>
          <Logo className='h-full w-full'/>
        </div>
        <h1 className='text-2xl font-bold text-center'>Story Title</h1>
        <div className="flex items-center justify-center gap-8">
          <img src="/left.png" className='w-20'></img>
          <img src="https://placehold.co/1000x500"></img>
          <img src="/next.png" className='w-20'></img>
        </div>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
      </div>
    </>
  )
}

export default StoryDetailPage