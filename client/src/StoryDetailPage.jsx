import React, { useEffect, useState} from 'react'
import {ReactComponent as Logo} from './logo.svg'
import ProgressBar from './ProgressBar';
import { useNavigate, useParams } from 'react-router-dom'
import KidResponseRecorder from './KidResponseRecorder';



const StoryDetailPage = () => {
  const { pageId } = useParams();
  const navigate = useNavigate(); 

  const [story, setStory] = useState('');
  const [currentPage, setCurrentPage] = useState(parseInt(pageId, 10));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audio, setAudio] = useState(null);
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false);

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
      setAudioUrl(`http://127.0.0.1:5000/${story.voice_links[parseInt(currentPage, 10) - 1]}`);
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

  const getNextTwoIllustrations = () =>{
    fetch('/next_page', {
      method: 'GET',
    }).then(res => res.json())
    .then(data => {
      console.log(data);
    }).catch(error=>{
      console.log(error);
    })
  }

  useEffect(() => {
    playAudio();
  }, [story])

  const playAudio = () =>{
    if (audioUrl) {
      const audioObj = new Audio(audioUrl);
      setAudio(audioObj);
      audioObj.play();
    }
  }

  const handleNextPage = () => {
    if (audio) {
      audio.pause();
    }
    const nextPageId = currentPage + 1;;
    if (nextPageId > story.pages) {
      navigate('/story_gallery');
    } else {
      setCurrentPage(nextPageId);
      navigate(`/story/${nextPageId}`);
      getNextTwoIllustrations();
    }
  };

  const handlePreviousPage = () => {
    if (audio) {
      audio.pause();
    }
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
    {loading && <span className="loading loading-dots loading-sm"></span>}
    {error && <p>{error}</p>}
    {story && (
        <div className='flex flex-col items-center justify-start min-h-screen gap-4'>
          <div className='h-40 w-full'>
            <Logo className='h-full w-full'/>
          </div>
          <div className='flex flex-col items-center justify-center gap-8'>
            <ProgressBar pages={story.pages} currentPage={currentPage}/>
            <h1 className='text-2xl font-bold text-center'>{story.title}</h1>
            <div className="flex flex-row items-center justify-center px-2">
              <button disabled={currentPage === 1} onClick={handlePreviousPage}>
                <img 
                  src="/left.png" 
                  className={`w-20  ${currentPage === 1 ? 'opacity-20 cursor-not-allowed' : 'cursor-pointer hover:bg-base-200'}`} 
                  alt="previous page"></img>
              </button>
              
              {/* display the current illustration here */}
              <figure className='px-4 w-[1000px] h-[500px]'>
                <img className='object-cover w-full h-full'  src={`http://127.0.0.1:5000/static/img/${story.illustration_links[parseInt(currentPage, 10) - 1]}`} alt="story illustration"></img>
              </figure>

              <button onClick={handleNextPage}>
                <img 
                  src="/next.png" 
                  className='w-20 hover:bg-base-200 cursor-pointer' 
                  alt="next page"></img>
              </button>
            </div>
            <div className="max-w-7xl flex flex-col items-center justify-center gap-6">
                <p>{story.parts[currentPage - 1]}</p>
            </div>
            
            {/* interaction window */}
            <div className="flex justify-between" >
              {/* voic character */}
              <div className="chat chat-start">
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full">
                    <img
                      alt="Tailwind CSS chat bubble component"
                      src={story.voice_charcater["voice_character_path"]}
                    />
                  </div>
                </div>
                <div className="chat-header">
                  {story.voice_charcater["voice_character"]}
                </div>
                <div className="chat-bubble">{story.question}</div>
              </div>

              {/* kid's response */}
              <div className="chat chat-end">
                {/* <button className="btn btn-circle" onClick={() => setShowVoiceRecorder(true)}>
                  <img src="/mic.svg" alt="speakIcon" />
                </button> */}
                <KidResponseRecorder />
              </div>
            </div>

          </div>
        </div>
        )}
  </>
  )
}

export default StoryDetailPage