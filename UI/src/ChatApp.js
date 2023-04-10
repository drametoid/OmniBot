import React, { useState } from 'react';
import './ChatApp.css';
import userAvatar from './user-avatar.png';
import botAvatar from './bot-avatar.jpeg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faUpload } from '@fortawesome/free-solid-svg-icons';


const ChatApp = () => {
  const [newMessage, setNewMessage] = useState('');
  const [image, setImage] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userResponse, setuserResponse] = useState('prompt');
  const [category, setCategory] = useState('');

  const fakeMessages = [
    { id: 1, text: 'Hi there! What can I do for you', sender: 'bot', avatar: botAvatar },
  ];
  const [messages, setMessages] = useState(fakeMessages);
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(image);
      if (image) {
      setMessages(prevMessages => [
        ...prevMessages,
        { id: prevMessages.length + 1, text: image.name, sender: 'user', avatar: userAvatar }
      ]);
      }
      else{
        setMessages(prevMessages => [
          ...prevMessages,
          { id: prevMessages.length + 1, text: newMessage, sender: 'user', avatar: userAvatar }
        ]);
      }
      let shouldUpdateState = false;
      let jsonObject = {};
      if(userResponse === 'prompt'){
        setIsLoading(true);
        var requestOptions = {
          method: 'GET',
          redirect: 'follow'
        };
        fetch(`http://3.14.131.137:8000/model_get_category/?prompt=${newMessage}`, requestOptions)
          .then(response => response.text())
          .then(result => {
            console.log(result);
            jsonObject = JSON.parse(result);
            shouldUpdateState = true;
          })
          .catch(error => console.log('error', error))
          .finally(() => {
            if(shouldUpdateState){
              // setUserInput(category);
              setCategory(jsonObject['category']);
              let msg = '';
              setIsLoading(false);
              switch(jsonObject['category']) {
                case 'blog':
                  msg = 'Sure! Can you provide the link for the blog?';
                  setuserResponse('input');
                  break;
                case 'resume':
                  msg = 'Sure! Can you provide the pdf file for your resume?';
                  setuserResponse('input');
                  break;
                  case 'suduko':
                    msg = 'Sure! Can you provide the image for your suduko puzzle?';
                    setuserResponse('input');
                    break;
                    case 'audio_to_text':
                      msg = 'Sure! Can you provide the audio with .wav extension?';
                      setuserResponse('input');
                      break;
                    default:
                      msg = 'Sorry, I am not sure. Could you please provide another prompt?';
                      setuserResponse('prompt');
              }
              setMessages(prevMessages => [
                ...prevMessages,
                { id: prevMessages.length + 1, text: msg, sender: 'bot', avatar: botAvatar }
              ]);
            }
          });
      }
      if(userResponse === 'input'){
        setIsLoading(true);
        let url = '';
        let res = '';
        let formdata = new FormData();
        switch(category) {
          case "blog":
            formdata.append("medium_link", newMessage);
            console.log(formdata)
            url = 'http://3.14.131.137:8000/model_get_blog_summary/'
            break;
          case "resume":
            formdata.append("resume",  image, "sample_resume.pdf");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_resume_summary/";
            break;
          case "suduko":
            formdata.append("suduko",  image, "sample_sudoku.jpeg");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_suduko/";
            break;
          case "audio_to_text":
            formdata.append("audio",  image, "audio.wav");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_audio_to_text/";
            break;
        }
        let requestOptions = {
          method: 'POST',
          body: formdata,
          redirect: 'follow'
        };
        fetch(`${url}`, requestOptions)
          .then(response => response.text())
          .then(result => {
            console.log(result);
            let jsonObject = JSON.parse(result);
            if(category === "audio_to_text"){
              res = jsonObject['transcript']
            }
            else{
              if(category === 'suduko'){
                res = `Here is the solution for the suduku puzzle you asked for: \n\n`
              }
              res += jsonObject['summary']
            }
            shouldUpdateState = true;
          })
          .catch(error => console.log('error', error))
          .finally(() => {
            if(shouldUpdateState){
              // setUserInput(category);
              setIsLoading(false);
                  setMessages(prevMessages => [
                    ...prevMessages,
                    { id: prevMessages.length + 1, text: res, sender: 'bot', avatar: botAvatar },
                    { id: prevMessages.length + 2, text: "What else I can do for you?", sender: 'bot', avatar: botAvatar }
                  ]);
                  setuserResponse('prompt');
            }
             setImage(null);
        setUploadedFileName('');
          });
       
      }
      setNewMessage('');
  };

    

  const handleFileInputChange = (event) => {
    console.log(event.target.files)
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
    accept="application/pdf, image/*, audio/wav"
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
