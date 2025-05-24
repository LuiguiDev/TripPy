import { useState } from 'react'
import Explorer from './explorer/Explorer'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Explorer />
    </>
  )
}

export default App
