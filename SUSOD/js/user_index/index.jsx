import React, {Component} from 'react';
import PropTypes from 'prop-types';


// THIS FILE WILL NEED TO BE CHANGED, here to test compilation

class Index extends Component {
	constructor() {
		super();
		this.state = {
			
		};
	}

	componentDidMount() {
		fetch(this.props.url, { credentials: 'same-origin'})
			.then((response) => {
				if (!response.ok) throw Error(response.statusText);
				return response.json();
			})
			.then((data) => {
				this.setState(data);
			});
	}

	render() {
		return (
			<div>
				<p>
					users stuff
				</p>
			</div>
		);
	}
}


Index.propTypes = {
	url: PropTypes.string.isRequired,
}


export default Index;