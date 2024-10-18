import React from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'
import {ReactComponent as Logo} from './logo.svg'

const StoryGalleryPage = () => {

  const navigate = useNavigate(); 
  const { name } = useOutletContext();


  return (
    <div className='flex flex-col items-center justify-start min-h-screen gap-6'>
      <div className='h-40 w-full'>
        <Logo className='h-full w-full'/>
      </div>
      <h1 className='text-3xl font-bold text-center'>Yu's Story Gallery</h1>

      {/* story cards here */}

      <div className='flex items-center justify-start gap-4 p-6'>

        <div className="card bg-base-100 w-96 shadow-xl">
          <figure className="px-10 pt-10">
            <img
              src="http://127.0.0.1:5000/static/img/test_generation_img.webp"
              alt="test-story-image"
              className="rounded-xl" />
          </figure>
          <div className="card-body items-center text-center">
            <h2 className="card-title">Story Title</h2>
            <p>Created on 2022-01-01</p>
            <div className="card-actions">
              <button className="btn btn-primary">Read</button>
            </div>
          </div>
        </div>

      </div>

    </div>  
    )
}

export default StoryGalleryPage