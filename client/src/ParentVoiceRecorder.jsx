import React, { useState, useEffect, useRef } from 'react';

const ParentVoiceRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const mediaRecorderRef = useRef(null);
  const chunks = useRef([]);

  useEffect(() => {
    if (isRecording) {
      // Start recording when `isRecording` is true
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          mediaRecorderRef.current = new MediaRecorder(stream);
          mediaRecorderRef.current.start();

          mediaRecorderRef.current.ondataavailable = (e) => {
            chunks.current.push(e.data);
          };

          mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(chunks.current, { type: 'audio/wav' });
            chunks.current = [];
            const audioURL = URL.createObjectURL(audioBlob);
            setAudioURL(audioURL);
            uploadAudio(audioBlob);  // Call function to upload audio
          };
        })
        .catch(err => {
          console.error('Error accessing microphone: ', err);
        });
    } else if (mediaRecorderRef.current) {
      // Stop recording when `isRecording` is false
      mediaRecorderRef.current.stop();
    }
  }, [isRecording]);

  // Function to handle recording start/stop
  const handleRecord = () => {
    setIsRecording(!isRecording);
  };

  // Function to upload audio to the server
  const uploadAudio = (audioBlob, audioName) => {
    const formData = new FormData();
    const audioFile = new File([audioBlob], "parent_recording.wav", { type: 'audio/wav' });
    formData.append('audio', audioFile);

    fetch('/upload-audio', {
      method: 'POST',
      body: formData,
    })
      .then(response => {
        if (response.ok) {
          console.log('Audio uploaded successfully');
        } else {
          console.error('Failed to upload audio');
        }
      })
      .catch(err => console.error('Error uploading audio:', err));
  };

    return (
      <div className='flex flex-col items-center justify-center gap-6'>
        <button className='btn btn-secondary' onClick={handleRecord}>
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>

        {audioURL && (
          <div className='flex flex-col items-center justify-center gap-2'>
            <h2>Recorded Audio: </h2>
            <audio controls src={audioURL}></audio>
          </div>
        )}
      </div>
    );
};

export default ParentVoiceRecorder;