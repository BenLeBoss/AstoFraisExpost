import { createBrowserRouter } from 'react-router-dom'

import Authentif from './Pages/Auth/Page_Authentification'
import Selection_Fournisseur from './Pages/Main/Page_SelectionFournisseurs'
import Generation_Fiche_Fournisseur from './Pages/Main/Page_Fournisseur'
import Consultation_FichesGenerees from './Pages/Main/Page_Consultation_FichesGenerees'
import Consultation_FichesNonGenerees from './Pages/Main/Page_Consultation_FichesNonGenerees'

const router = createBrowserRouter(
  [
    { path: '/', element: <Authentif/> },
    { path: '/menu', element: <Selection_Fournisseur/> },
    { path: '/partenaire', element: <Generation_Fiche_Fournisseur/> },
    { path: '/client/consultation/fichesgenerees', element: <Consultation_FichesGenerees/> },
    { path: '/client/consultation/fichesnongenerees', element: <Consultation_FichesNonGenerees/> },
  ],
  {
    future: {
      v7_startTransition: true,
      v7_relativeSplatPath: true,
    },
  }
)

export default router
