import { useState } from 'react'
import './App.css'

function App() {
  const [todos, setTodos] = useState([])
  const [inputValue, setInputValue] = useState('')

  const handleAddTodo = () => {
    // Prevent adding empty todos
    if (inputValue.trim() === '') return; 

    // Create a new todo object with a unique ID and the text
    const newTodo = {
      id: Date.now(), 
      text: inputValue
    };

    setTodos([...todos, newTodo])
    setInputValue('')
  }

  const handleDeleteTodo = (id) => {
    const updatedTodos = todos.filter((todo) => todo.id !== id)
    setTodos(updatedTodos)
  }

  return (
    <div className="app-container">
      <h2>My Todo List</h2>
      
      <div className="input-section">
        <input 
          type="text" 
          value={inputValue} 
          onChange={(e) => setInputValue(e.target.value)} 
          placeholder="What needs to be done?"
          onKeyDown={(e) => e.key === 'Enter' && handleAddTodo()}
        />
        <button onClick={handleAddTodo} className="add-btn">Add</button>
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          // The key goes on the outermost element (the li)
          <li key={todo.id}>
            <span>{todo.text}</span>
            <button onClick={() => handleDeleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
        {todos.length === 0 && <p className="empty-msg">No todos yet. Add one above!</p>}
      </ul>
    </div>
  )
}

export default App