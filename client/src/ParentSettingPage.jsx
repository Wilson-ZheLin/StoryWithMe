import React from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'


const ParentSettingPage = () => {
    
    const navigate = useNavigate(); 
    const {name, setName, age, setAge, readTime, setReadTime, hobbies, setHobbies} = useOutletContext()

    const handleHobbies = (index, value) =>{
        const newHobbies = [...hobbies];
        newHobbies[index] = value;
        setHobbies(newHobbies);
    }

    const onSubmit = () => {
        navigate('/welcome')
    }

  return (
    <>
        <h1 className='text-3xl font-bold pt-12 text-center'>Welcome to StoryWithMe!</h1>
        <div className="flex flex-col items-center justify-start min-h-screen gap-6 p-9">
            <h2 className="text-2xl">Parent Settings</h2>
            <p>Please provide the following details of your child:</p>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Name: *</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    value={name}
                    onChange={(e) => setName(e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Age: *</label>
                <input
                    type="number"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    value={age}
                    onChange={(e) => setAge(e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Read Time: *</label>
                <input
                    type="number"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    placeholder='minutes'
                    value={readTime}
                    onChange={(e) => setReadTime(e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Hobby 1:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[0]}
                    onChange={(e) => handleHobbies(0, e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Hobby 2:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[1]}
                    onChange={(e) => handleHobbies(1, e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4'>
                <label className='w-36'>Hobby 3:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[2]}
                    onChange={(e) => handleHobbies(2, e.target.value)} />
            </div>
            <div className='flex flex-col items-center justify-center gap-4'>
                <label className=''>Would you like to record your voice? If so, please click the microphone</label>
                {/* TODO: enable voice sample recording */}
                <img src="/mic.svg" alt="mic" className="w-12 rounded-full bg-secondary hover:cursor-pointer" />
                <p>Sample Recording text</p>
            </div>
            <button
                className="btn btn-primary"
                onClick={onSubmit}>
                    Submit
            </button>
        </div>
    </>
  )
}

export default ParentSettingPage