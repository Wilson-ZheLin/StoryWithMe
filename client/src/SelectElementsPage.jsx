import React, { useEffect, useState} from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'

const SelectElementsPage = () => {

  const navigate = useNavigate();
  const {elements, setElements} = useOutletContext();
  const [images, setImages] = useState([]);

  // Fetch the json file with the image information
  useEffect(()=>{
      fetch('/elementData.json')
      .then(res => res.json())
      .then(data =>{
          setImages(data)
      })
      .catch((error)=>console.log(error))
  },[])

  // Helper function to extract the image name
  const getImageName = (src) => {
      const fileName = src.split('/').pop(); // Get the file name from the path
      return fileName.split('.')[0]; // Remove the extension and return the name
  };

  // Handle element change
  const addElement = (newElement) => {
      setElements((prevElements) => [...prevElements, newElement]);
  };
  
    useEffect(() => {
      console.log(elements);
    }, [elements]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-6">
      <h1 className="text-3xl font-bold text-center">Slect 3-5 elements for your story:</h1>
      <div className="grid grid-cols-4 gap-4 p-4">
        {images.map((image, index) => (
            <div key={index} className="flex items-center">
                <img src={`/${image.src}`}
                    alt={getImageName(image.src)}
                    className={`w-36 h-36 object-cover hover:bg-base-200 cursor-pointer ${elements.includes(getImageName(image.src)) ? 'bg-base-200' : ''}`}
                    onClick={(e) => {
                        const newElement = getImageName(e.target.src);
                        if (elements.includes(newElement)) {
                            setElements(elements.filter(element => element !== newElement));
                        } else {
                            setElements([...elements, newElement]);
                        }
                    }}
                    />
            </div>
        ))}
      </div>
      <button className='btn btn-primary' onClick={() => navigate('/voice_select')}>Next</button>
    </div>
  )
}


export default SelectElementsPage