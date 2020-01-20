import React from 'react'
import DataProvider from '../../components/dataProvider'
import Table from '../../components/table'
import {BrowserRouter} from 'react-router-dom'

const TransactionList = () => {
  return (
    <div>
      <h1>Transactions</h1>
      <DataProvider
        endpoint="../api/transactions/"
        render={data => <Table data={data} />}
      />
    </div>
  )
}

export default TransactionList
