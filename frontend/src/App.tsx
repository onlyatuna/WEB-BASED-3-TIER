import React, { useState } from 'react';
import MainPage from './pages/MainPage';
import UserPage from './pages/UserPage';
import CustPage from './pages/CustPage';
import FactPage from './pages/FactPage';
import ItemPage from './pages/ItemPage';

type Page = 'main' | 'user' | 'cust' | 'fact' | 'item';

const App: React.FC = () => {
  const [page, setPage] = useState<Page>('main');

  const back = () => setPage('main');

  return (
    <>
      {page === 'main' && <MainPage onNav={setPage} />}
      {page === 'user' && <UserPage onBack={back} />}
      {page === 'cust' && <CustPage onBack={back} />}
      {page === 'fact' && <FactPage onBack={back} />}
      {page === 'item' && <ItemPage onBack={back} />}
    </>
  );
};

export default App;
