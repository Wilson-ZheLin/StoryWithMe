import React, { useState, useEffect } from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'
import ParentVoiceRecorder from './ParentVoiceRecorder';


const ParentSettingPage = () => {
    
    const navigate = useNavigate(); 
    const {name, setName, age, setAge, readTime, setReadTime, hobbies, setHobbies, parentVoice, setParentVoice} = useOutletContext()

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
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Name: *</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    value={name}
                    onChange={(e) => setName(e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Age: *</label>
                <input
                    type="number"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    min={3}
                    max={8} />
            </div>
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Read Time: *</label>
                <input
                    type="number"
                    className="input input-bordered input-primary w-full max-w-xs required:border-red-500"
                    placeholder='minutes (min)'
                    value={readTime}
                    onChange={(e) => setReadTime(e.target.value)}
                    min={1}
                    max={5} />
            </div>
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Hobby 1:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[0]}
                    onChange={(e) => handleHobbies(0, e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Hobby 2:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[1]}
                    onChange={(e) => handleHobbies(1, e.target.value)} />
            </div>
            <div className='flex items-center justify-center gap-4 w-[400px]'>
                <label className='w-36'>Hobby 3:</label>
                <input
                    type="text"
                    className="input input-bordered input-primary w-full max-w-xs"
                    value={hobbies[2]}
                    onChange={(e) => handleHobbies(2, e.target.value)} />
            </div>
            <div className='flex flex-col items-center justify-center gap-4 px-52 w-4/5'>
                <p className='font-bold'>If you'd like, you can record your voice here to be used in the story:</p>
                <p>Once upon a time, a little bird named Pip lived in a cozy nest high up in a big oak tree. One sunny morning, Pip wanted to learn how to fly. “Flap your wings!” his friends chirped. So Pip flapped and flapped, but he was too scared to jump. Then, his best friend, a squirrel named Nutty, said, “I’ll be right here to catch you if you fall!” Pip took a deep breath, flapped his wings, and leaped from the branch. To his surprise, he soared through the sky! Pip flew in circles, happy and proud, knowing his friends would always be there to cheer him on. And from that day on, Pip never stopped flying!</p>
                <div className='flex gap-6'>
                    <ParentVoiceRecorder />
                </div>
                <div className="form-control">
                <label className="cursor-pointer label">
                    <input type="checkbox" className="checkbox checkbox-info" />
                    <span className="label-text pl-5">By checking this box, I consent to the use of my input data and voice recordings for AI story generation, understanding that my data will be handled responsibly and securely</span>
                </label>
                </div>
            </div>
            <button
                className="btn btn-primary mt-6"
                onClick={onSubmit}>
                    Submit
            </button>
        </div>
    </>
  )
}

export default ParentSettingPage