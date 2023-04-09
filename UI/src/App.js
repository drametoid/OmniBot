// import config from './Components/Config';
// import './App.css';
// import Chatbot from "react-chatbot-kit";
// import ActionProvider from "./Components/ActionProvider";
// import MessageParser from "./Components/MessageParser";

// function App() {
//   return (
//     <div className="App">
//     <header className="App-header">
//     <Chatbot
//     config={config}
//           actionProvider={ActionProvider}
//           messageParser={MessageParser}
//   />
//     </header>
    
//     </div>
//   );
// }

// export default App;

import ChatApp from './ChatApp';
import './App.css';

function App() {
  return (
    <div className="App">
    <header className="App-header">
    <ChatApp
  />
    </header>
    
    </div>
  );
}

export default App;
