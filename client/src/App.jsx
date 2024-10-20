import React, { useState } from 'react'
import {Outlet} from 'react-router-dom'

const App = () => {

  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [readTime, setReadTime] = useState('');
  const [hobbies, setHobbies] = useState([]);
  const [elements, setElements] = useState([]);
  const [mood, setMood] = useState('');
  const [voiceCharacter, setVoiceCharacter] = useState('');
  const [voiceCharacterPath, setVoiceCharacterPath] = useState('');
  const [parentVoice, setParentVoice] = useState(false);


  const stateProps = {
    name, setName,
    age, setAge,
    readTime, setReadTime,
    hobbies, setHobbies,
    elements, setElements,
    mood, setMood,
    voiceCharacter, setVoiceCharacter,
    voiceCharacterPath, setVoiceCharacterPath,
    parentVoice, setParentVoice
  };

  return (
    <>
      <Outlet context={stateProps} />
      
      {/* display for testing */}
      <div className="flex flex-col justify-left p-2">
        <p>Name: {name}</p>
        <p>Age: {age}</p>
        <p>Readtime: {readTime}</p>
        <p>Hobbies: {hobbies}</p>
        <p>Elements: {elements}</p>
        <p>Mood: {mood}</p>
        <p>Voice: {voiceCharacter}</p>
        <p>Parent voice: {parentVoice}</p>

      </div>

    </>

  )
}

export default App