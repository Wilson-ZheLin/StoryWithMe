import {createBrowserRouter} from 'react-router-dom';

import App from '../App';
import ParentSettingPage from '../ParentSettingPage';
import WelcomePage from '../WelcomePage';
import MoodCheckPage from '../MoodCheckPage';
import SelectElementsPage from '../SelectElementsPage';
import GenerateStoryPage from '../GenerateStoryPage';
import StoryPage from '../StoryPage';
import StoryGalleryPage from '../StoryGalleryPage';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {path: '/', element: <ParentSettingPage /> },
            {path: 'welcome', element: <WelcomePage />},
            {path: 'mood_check', element: <MoodCheckPage />},
            {path: 'element_select', element: <SelectElementsPage />},
            {path: 'story', element: <GenerateStoryPage />},
            {path: 'story/:pageId', element: <StoryPage />},
            {path: 'story_gallery', element: <StoryGalleryPage />},
        ]
    }
]);
