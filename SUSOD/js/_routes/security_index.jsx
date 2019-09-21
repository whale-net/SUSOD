import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from 'security_index/index';



ReactDOM.render(
	<Index url="/api/security/" />,
	document.getElementById('reactEntry')
);

