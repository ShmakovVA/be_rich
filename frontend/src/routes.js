import React from 'react'
import {Switch, Route} from 'react-router-dom'
import TransactionList from './pages/transactionList'
import Transaction from './pages/transaction'
import Authentication from './pages/authentication'

export default () => {
  return (
    <Switch>
      <Route path="/" component={TransactionList} exact />
      <Route path="/login" component={Authentication} />
      <Route path="/register" component={Authentication} />
      <Route path="/pay" component={Transaction} />
    </Switch>
  )
}
