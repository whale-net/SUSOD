import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from 'transactions_index/index';



ReactDOM.render(
	<Index url="/api/transactions/" />,
	document.getElementById('reactEntry')
);
				