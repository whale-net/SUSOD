import React, {Component} from 'react';
import PropTypes from 'prop-types';


class Receipt extends React.Component {
	constructor(props) {
	  super(props);

	  this.state = {
	  	data: {}
	  }
	}
	
	componentDidMount() {
		fetch(this.props.url, {
				credentials: 'same-origin',
				method: 'POST',
				header: 'Content-Type: application/json',
				body: JSON.stringify(this.props.id)
			})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				console.log(data['receipt'][0]);
				this.setState({data: data['receipt'][0]});
			})
			.catch((error) => {
				console.log(error);
			});

	}

	render() {
		return (
			<span>
				<h1>{this.props.id}</h1>
				<h3>{this.state.data.Description}</h3>
			</span>
		)
	}
}


Receipt.propTypes = {
	url: PropTypes.string.isRequired,
	id: PropTypes.number

}


export default Receipt;
