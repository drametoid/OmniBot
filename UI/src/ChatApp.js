import React, { useState, useEffect } from 'react';
import './ChatApp.css';
import userAvatar from './user-avatar.png';
import botAvatar from './bot-avatar.jpeg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faUpload } from '@fortawesome/free-solid-svg-icons';


const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [image, setImage] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [prompt, setPrompt] = useState('');
  const [link, setLink] = useState('');
  const [isLoading, setIsLoading] = useState(true);

 
  // This useEffect hook will simulate fetching messages from a backend.
  useEffect(() => {
    const fakeMessages = [
      { id: 1, text: 'Hello!', sender: 'user', avatar: userAvatar },
      { id: 2, text: 'Hi there!', sender: 'bot', avatar: botAvatar },
      { id: 3, text: 'What can I do for you?', sender: 'bot', avatar: botAvatar },
      { id: 4, text: "Can you summarize this Medium blog for me?", sender: 'user', avatar: userAvatar },
      { id: 5, text: 'Sure, Please enter the URL for the blog.', sender: 'bot', avatar: botAvatar },
      { id: 6, text: "MEDIUM_LINK: https://medium.com/sfu-cspmp/the-artistic-potential-of-ai-understanding-dall-e-2-and-stable-diffusion-10a82e6965c0", sender: 'user', avatar: userAvatar },
      // { id: 7, text: '<div class="title">The Artistic Potential of AI: Understanding DALL-E 2 and Stable Diffusion</div><div class="sub-title">Written by Machine Minds on Feb 11</div><div class="heading">An Overview</div><div>AI is transforming the digital world by allowing machines to act and think like humans. Generative AI takes this a step further, introducing the ability to craete visuals, texts, sounds or songs. Models such as DALL-E 2 and Stable Diffusion, developed by OpenAI and LMU Munich respectively, use transformer-based designs and extensive training data to generate images from verbal descriptions, pushing the boundaries of creativity. AI has something to offer for everyone, with endless possibilities in store.<div>  \n <div class="heading">The Technology Behind DALL-E 2 </div>', sender: 'bot', avatar: botAvatar },
    ];
    setMessages(fakeMessages);
    const fetchMessages = async () => {
      // Fetch messages from the API
        var requestOptions = {
          method: 'GET',
          redirect: 'follow'
        };
      fetch(`http://13.58.199.27:8000/model_switcher_test/?prompt=Can you summarize this Medium blog for me?&medium_link=https://medium.com/sfu-cspmp/the-artistic-potential-of-ai-understanding-dall-e-2-and-stable-diffusion-10a82e6965c0`, requestOptions)
          .then(response => response.text())
          .then(results => {
            console.log(results);
            let jsonObject = JSON.parse(results)
            console.log(jsonObject);
            setMessages(prevMessages => [
              ...prevMessages,
              { id: prevMessages.length + 1, text: jsonObject['summary'], sender: 'bot', avatar: botAvatar }
            ]);
            // fakeMessages.push({id: fakeMessages.length + 1, text: jsonObject['summary'], sender: 'bot', avatar: botAvatar})
            
          })
          .catch(error => console.log('Failed to fetch messages', error))
          .finally(() => {
            setIsLoading(false)
          })
    };

    fetchMessages();
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (image) {
      const newMessageObj = {
        id: messages.length + 1,
        image: URL.createObjectURL(image),
        sender: 'user',
        avatar: userAvatar,
      };
      setMessages([...messages, newMessageObj]);
      setImage(null);
      setUploadedFileName('');
    }
    if (newMessage.trim()) {
      const newMessageObj = {
        id: messages.length + 1,
        text: newMessage,
        sender: 'user',
        avatar: userAvatar,
      };
      setMessages([...messages, newMessageObj]);
      if(newMessage.includes('summarize this Medium blog')){
        setPrompt('Can you summarize this Medium blog for me?')
      }
      if(newMessage.upper().includes('MEDIUM_LINK')){
        setLink('https://medium.com/sfu-cspmp/the-artistic-potential-of-ai-understanding-dall-e-2-and-stable-diffusion-10a82e6965c0')
      }
      setNewMessage('');
      setTimeout(() => {
        const botResponse = {
          id: messages.length + 2,
          text: `Sorry, I don't understand. Could you please rephrase that?`,
          sender: 'bot',
          avatar: botAvatar,
        };
        setMessages([...messages, botResponse]);
      }, 1000);
    }
  };

  const handleFileInputChange = (event) => {
    setImage(event.target.files[0]);
    setUploadedFileName(event.target.files[0].name);
  };

  return (
    <div className="chat-container">
      <div className='header'>
      <div style={{color: '#fff', padding:'10px', fontSize: "32px", fontWeight: 'bold'}}>OmniBot</div>
      </div>
      <div className="message-container">
        {messages.map((message) => (
          <div>
          <div key={message.id} className={`message ${message.sender}`}>
            <img src={message.avatar} alt="Avatar" className="avatar" />
            <div className="message-content">
              {message.text && <div style={{whiteSpace: 'pre-line', verticalAlign: 'bottom'}} dangerouslySetInnerHTML={{__html:message.text}}></div>}
              {message.image && <img src={message.image} alt="User uploaded" />}
            </div>
          </div>
          </div>
        ))}
        <div>
          {isLoading ? (
            // Show loader while data is being fetched
            <div className='loading' style={{ display: 'flex', alignItems: 'center' }}><img src={botAvatar} alt="Avatar" className="avatar" /> is typing...</div>
          ) : null}</div>
      </div>
      <div className='footer'>
      <form onSubmit={handleSubmit}>
  <input
    type="text"
    placeholder={uploadedFileName ? uploadedFileName : 'Type your message...'}
    value={newMessage}
    onChange={(event) => setNewMessage(event.target.value)}
    style={{ width: '300px' }}
  />
  <label htmlFor="file-input">
    <FontAwesomeIcon icon={faUpload} style={{ color: '#376B7E', margin: '8px' }} />
  </label>
  <input
    id="file-input"
    type="file"
    accept="image/*"
    onChange={handleFileInputChange}
    style={{ display: 'none' }}
  />
  <button type="submit">
    <FontAwesomeIcon icon={faPaperPlane} style={{ color: 'white' }} />
  </button>
</form>
</div>
</div>
  );
};

export default ChatApp;
