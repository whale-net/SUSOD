import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

// _header


class Header extends Component {

	static getMenuOptions(callback) {
		fetch('/api/_header/', {credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				callback(data);
			})
			.catch(error => console.log(error));
	}

	constructor(props) {
		super(props);
		this.state = {
			menuOptions: null
		};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.initMenuOptionState = this.initMenuOptionState.bind(this);
	}

	componentWillMount() {
		// REST api calls
		Header.getMenuOptions(this.initMenuOptionState);
	}

	handleChange(event) {
		this.setState({});
	}

	handleSubmit(event) {
		event.preventDefault();
	}

	initMenuOptionState(data) {
		// TODO make this merge not re-assign
		this.setState({
			menuOptions: data
		});
	}

	render() {
		// prevent render until after fetch
		if (!this.state.menuOptions)
			return <div />

		// TODO: make key not based on pk of db?
		const menuOptionList = [];
		this.state.menuOptions.forEach((option) => {
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