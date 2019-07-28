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
		// REST api calls
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