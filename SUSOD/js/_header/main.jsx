import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Navbar from 'react-bootstrap/Navbar';

// _header


class Header extends Component {
	constructor(props) {
		super(props);
		this.state = {
			
		};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	componentDidMount() {
		// REST api calls
	}

	handleChange(event) {
		this.setSate({

		});
	}

	handleSubmit(event) {
		event.preventDefault();
	}

	render() {
		return (
			<div>test123</div>
			// <Navbar bg="dark">
			// 	<Navbar.Brand>test123</Navbar.Brand>
			// </Navbar>
		);
	}
}


Header.propTypes = {
}


export default Header;