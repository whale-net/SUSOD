import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

// _header


class Header extends Component {

	constructor(props) {
		super(props);
		this.state = {};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.initState = this.initState.bind(this);
	}

	componentWillMount() {
		// REST api calls
		//Header.getInitialState(this.initState);
		fetch('/api/_header/', {credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.initState(data);
			})
			.catch(error => console.log(error));
	}

	handleChange(event) {
		this.setState({});
	}

	handleSubmit(event) {
		event.preventDefault();
	}

	initState(data) {
		// use this function to set up initial state
		this.setState(data);
	}

	render() {
		// prevent render until after fetch
		if (!this.state.menu)
			return <div />
		console.log(this.state);
		// TODO: make key not based on pk of db?
		const menuOptionList = [];
		this.state.menu.forEach((option) => {
			menuOptionList.push(
				<Nav.Item key={option.MenuOptionID}>
					<Nav.Link href={option.MenuLink}>{option.MenuText}</Nav.Link>
				</Nav.Item>
			);
		});

		return (
			<Navbar bg="dark" variant="dark">
				<Navbar.Brand>SUSOD</Navbar.Brand>
				<Nav fill className="mr-auto">
					{menuOptionList}
				</Nav>
			</Navbar>
		);
	}
}


Header.propTypes = {
}


export default Header;