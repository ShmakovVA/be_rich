import React, {Component} from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'

class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired,
    sort_by: PropTypes.string.isRequired,
    filters: PropTypes.object.isRequired
  }
  state = {
    data: [],
    token: localStorage.getItem('token'),
    loaded: false,
    placeholder: 'Please, log in or register to continue...'
  }

  getItems = (sort_by, filters) => {
    const token = 'Token '.concat(localStorage.getItem('token'))
    if (!token) {
      return {}
    }
    axios
      .get(this.props.endpoint, {
        headers: {Authorization: token},
        params: {sort_by: sort_by, filters: filters}
      })
      .then(response => {
        let data = response.data
        if (response.data.results) {
          data = data.results
        }
        if (this.props.endpoint.includes('transactions')) {
          for (var i = 0; i < data.length; i++) {
            data[i].from_wallet = data[i].from_wallet.wallet_id
            data[i].to_wallet = data[i].to_wallet.wallet_id
          }
        }
        if (this.props.endpoint.includes('wallets')) {
          for (var i = 0; i < data.length; i++) {
            data[i].account = data[i].account.user.email
          }
        }
        if (this.props.endpoint.includes('accounts')) {
          for (var i = 0; i < data.length; i++) {
            data[i].user = data[i].user.email
          }
        }
        this.setState({data: data, loaded: true})
      })
      .catch(exception => {
        let error = exception.toJSON()
        console.log(error)
        // alert(error.message)
      })
  }

  componentDidMount() {
    this.getItems(this.props.sort_by, this.props.filters) // {'message': '00'}
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (
      (this.props.sort_by !== prevProps.sort_by) |
      (this.props.filters !== prevProps.filters)
    ) {
      let sort_by_ = !this.props.sort_by ? 'id' : this.props.sort_by
      this.getItems(sort_by_, this.props.filters)
    }
  }

  render() {
    const {data, loaded, token, placeholder} = this.state
    return loaded ? this.props.render(data) : <p>{placeholder}</p>
  }
}

export default DataProvider
