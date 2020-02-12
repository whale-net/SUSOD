import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from 'pavlov_index/index';



ReactDOM.render(
	<Index url="/api/pavlov/" />,
	document.getElementById('reactEntry')
);
				