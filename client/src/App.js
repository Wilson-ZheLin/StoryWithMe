import React, { useState, useEffect } from 'react'

const App = () => {

  const [data, setData] = useState({})
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [age, setAge] = useState(0);
  const [readTime, setReadTime] = useState(0);
  const [elements, setElements] = useState([]);

  // Fetching data from backend
  const fetchData = () => {
    setLoading(true);
    fetch('/story', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ age, readTime, elements })
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

  // Handle element change
  const handleElementChange = (index, value) => {
    const newElements = [...elements];
    newElements[index] = value;
    setElements(newElements);
  };

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className='text-3xl font-bold'>Welcome to StoryWithMe!</h1>
      <div className='flex items-center justify-center gap-4'>
        <label className='w-32'>Age:</label>
        <input
          type="number"
          className="input input-bordered input-primary w-full max-w-xs"
          value={age}
          onChange={(e) => setAge(e.target.value)} />
      </div>
      <div className='flex items-center justify-center gap-4'>
        <label className='w-32'>Read Time:</label>
        <input
          type="number"
          className="input input-bordered input-primary w-full max-w-xs"
          value={readTime}
          onChange={(e) => setReadTime(e.target.value)} />
      </div>
      <div className='flex items-center justify-center gap-4'>
        <label className='w-32'>Element 1:</label>
        <input
          type="text"
          className="input input-bordered input-primary w-full max-w-xs"
          value={elements[0]}
          onChange={(e) => handleElementChange(0, e.target.value)} />
      </div>
      <div className='flex items-center justify-center gap-4'>
        <label className='w-32'>Element 2:</label>
        <input
          type="text"
          className="input input-bordered input-primary w-full max-w-xs"
          value={elements[1]}
          onChange={(e) => handleElementChange(1, e.target.value)} />
      </div>
      <div className='flex items-center justify-center gap-4'>
        <label className='w-32'>Element 3:</label>
        <input
          type="text"
          className="input input-bordered input-primary w-full max-w-xs"
          value={elements[2]}
          onChange={(e) => handleElementChange(2, e.target.value)} />
      </div>

      <button
        className="btn btn-primary"
        onClick={fetchData}>Generate Story</button>
      {loading && <span className="loading loading-dots loading-sm"></span>}
      {error && <p>{error}</p>}
      {data && (
        <div className="max-w-7xl">
          <p>{data.story}</p>
        </div>
      )}
    </div>
  )
}

export default App