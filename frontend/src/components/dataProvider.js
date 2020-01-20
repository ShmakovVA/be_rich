import React, {Component} from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'

class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  }
  state = {
    data: [],
    token: localStorage.getItem('token'),
    loaded: false,
    placeholder: 'Please, log in or register to continue...'
  }

  inUrl = (endpoint, val) => {
    return endpoint.includes(val)
  }

  getTransactions = sort_by => {
    const token = 'Token '.concat(localStorage.getItem('token'))
    if (!token) {
      return {}
    }
    axios
      .get(this.props.endpoint, {
        headers: {Authorization: token},
        params: {sort_by: sort_by}
      })
      .then(response => {
        if (response.status !== 200) {
          this.setState({placeholder: 'Something went wrong'})
        }
        let data = response.data
        if (response.data.results) {
          data = data.results
        }
        if (this.inUrl(this.props.endpoint, 'transactions')) {
          for (var i = 0; i < data.length; i++) {
            data[i].from_wallet = data[i].from_wallet.wallet_id
            data[i].to_wallet = data[i].to_wallet.wallet_id
          }
        }
        if (this.inUrl(this.props.endpoint, 'wallets')) {
          for (var i = 0; i < data.length; i++) {
            data[i].account = data[i].account.user.email
          }
        }
        if (this.inUrl(this.props.endpoint, 'accounts')) {
          for (var i = 0; i < data.length; i++) {
            data[i].user = data[i].user.email
          }
        }

        return data
      })
      .then(data => this.setState({data: data, loaded: true}))
  }

  componentDidMount() {
    this.getTransactions('message')
  }

  render() {
    const {data, loaded, token, placeholder} = this.state
    return loaded ? this.props.render(data) : <p>{placeholder}</p>
  }
}

export default DataProvider
