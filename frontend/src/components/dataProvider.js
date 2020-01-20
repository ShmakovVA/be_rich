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
    placeholder: 'Loading...'
  }

  componentDidMount() {
    const token = 'Token '.concat(localStorage.getItem('token'))
    if (!token) {
      return {}
    }
    axios
      .get(this.props.endpoint, {headers: {Authorization: token}})
      .then(response => {
        if (response.status !== 200) {
          this.setState({placeholder: 'Something went wrong'})
        }
        let data = response.data.results
        for (var i = 0; i < data.length; i++) {
          data[i].from_wallet = data[i].from_wallet.wallet_id
          data[i].to_wallet = data[i].to_wallet.wallet_id
        }
        return data
      })
      .then(data => this.setState({data: data, loaded: true}))
  }

  render() {
    const {data, loaded, token, placeholder} = this.state
    return loaded ? this.props.render(data) : <p>{placeholder}</p>
  }
}

export default DataProvider
