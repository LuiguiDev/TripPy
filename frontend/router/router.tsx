import { Route, Routes} from "react-router-dom"
import { routes } from "./routes.config"



const routesConfig = routes

const Router = () => {
  return (
    <Routes>
      {
        routesConfig.map(r => (
          <Route path={r.path} element={r.commponent} />
        ))
      }
    </Routes>
  )
}

export default Router