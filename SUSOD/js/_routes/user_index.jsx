import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from 'user_index/index';



ReactDOM.render(
	<Index url="/api/user/" />,
	document.getElementById('reactEntry')
);

