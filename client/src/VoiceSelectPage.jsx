import React, { useEffect, useState} from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'


const VoiceSelectPage = () => {

    const navigate = useNavigate();
    const {voiceCharacter, setVoiceCharacter, voiceCharacterPath, setVoiceCharacterPath} = useOutletContext();
    const [selectedVoice, setSelectedVoice] = useState(null);

    const handleVoice = (e) => {
        setVoiceCharacter(e.target.alt);
        setSelectedVoice(e.target.alt);
        setVoiceCharacterPath(e.target.src);
    }

    const handleClick = () =>{
        navigate("/story");
    }

    useEffect(() => {
        console.log(voiceCharacter);
        console.log(voiceCharacterPath);
    }, [voiceCharacter]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-6">
      <h1 className="text-3xl font-bold text-center">Which friend would you like to create a story with?</h1>
      <div className="flex gap-3">
        <img
          src="/skyler.svg"
          alt="skyler"
          className={`w-36 cursor-pointer hover:bg-base-200 ${selectedVoice === 'skyler' ? 'bg-base-200' : ''}`}
          onClick={handleVoice}
        />
        <img
          src="/thor.svg"
          alt="thor"
          className={`w-36 cursor-pointer hover:bg-base-200 ${selectedVoice === 'thor' ? 'bg-base-200' : ''}`}
          onClick={handleVoice}
        />
        <img
          src="/olive.svg"
          alt="olive"
          className={`w-36 cursor-pointer hover:bg-base-200 ${selectedVoice === 'olive' ? 'bg-base-200' : ''}`}
          onClick={handleVoice}
        />
        <img
          src="/remy.svg"
          alt="remy"
          className={`w-36 cursor-pointer hover:bg-base-200 ${selectedVoice === 'remy' ? 'bg-base-200' : ''}`}
          onClick={handleVoice}
        />
      </div>
      <button className='btn btn-primary' onClick={handleClick}>Start my Story</button>
    </div>
  )
}

export default VoiceSelectPage