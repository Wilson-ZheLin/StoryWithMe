import {createBrowserRouter} from 'react-router-dom';

import App from '../App';
import ParentSettingPage from '../ParentSettingPage';
import WelcomePage from '../WelcomePage';
import MoodCheckPage from '../MoodCheckPage';
import SelectElementsPage from '../SelectElementsPage';
import GenerateStoryPage from '../GenerateStoryPage';
import StoryDetailPage from '../StoryDetailPage';
import StoryGalleryPage from '../StoryGalleryPage';
import VoiceSelectPage from '../VoiceSelectPage';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {path: '/', element: <ParentSettingPage /> },
            {path: 'welcome', element: <WelcomePage />},
            {path: 'mood_check', element: <MoodCheckPage />},
            {path: 'element_select', element: <SelectElementsPage />},
            {path: 'voice_select', element: <VoiceSelectPage />},
            {path: 'story', element: <GenerateStoryPage />},
            {path: 'story/:pageId', element: <StoryDetailPage />},
            {path: 'story_gallery', element: <StoryGalleryPage />},
        ]
    }
]);
