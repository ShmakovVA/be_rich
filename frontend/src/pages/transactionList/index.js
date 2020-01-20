import React from 'react'
import DataProvider from '../../components/dataProvider'
import Table from '../../components/table'

const TransactionList = () => {
  return (
    <div className="bg-secondary">
      <h1>Account(s)</h1>
      <DataProvider
        endpoint="../api/accounts/"
        render={data => <Table data={data} />}
      />
      <h1>Wallets</h1>
      <DataProvider
        endpoint="../api/wallets/"
        render={data => <Table data={data}/>}
      />
      <h1>Transactions</h1>
      <DataProvider
        endpoint="../api/transactions/"
        render={data => <Table data={data}/>}
      />
    </div>
  )
}

export default TransactionList
