import ChatWindow from "./components/ChatWindow";
import AuthGate from "./components/AuthGate";

function App() {
  return (
    <AuthGate>
      <ChatWindow />
    </AuthGate>
  );
}

export default App;