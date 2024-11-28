// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

import React from 'react';
import PropTypes from 'prop-types';
import { FiSmile, FiMeh, FiFrown } from 'react-icons/fi';

const style = {
  verticalAlign: 'middle',
};

export const SentimentIcon = ({ sentiment = 'NEUTRO', size = '1.5em' }) => {
  if (sentiment === 'POSITIVO') {
    return <FiSmile style={style} color="green" size={size} title="positive" />;
  }

  if (sentiment === 'NEGATIVO') {
    return <FiFrown style={style} color="red" size={size} title="negative" />;
  }

  return <FiMeh style={style} color="grey" size={size} tille={sentiment.toLowerCase()} />;
};
SentimentIcon.defaultProps = {
  sentiment: 'NEUTRO',
  size: '1.5em',
};
SentimentIcon.propTypes = {
  sentiment: PropTypes.oneOf(['POSITIVO', 'NEGATIVO', 'NEUTRO', 'MIX']),
  size: PropTypes.string,
};

const getSentimentColor = (sentiment) => {
  if (sentiment === 'POSITIVO') {
    return 'green';
  }
  if (sentiment === 'NEGATIVO') {
    return 'red';
  }
  return 'gray';
};

export const SentimentIndicator = ({ sentiment = 'NEUTRO' }) => (
  <div>
    <span>
      <SentimentIcon size="1.25em" sentiment={sentiment} />
    </span>
    <span style={{ verticalAlign: 'middle', padding: '3px', color: getSentimentColor(sentiment) }}>
      {` ${sentiment.charAt(0)}${sentiment.slice(1).toLowerCase()} `}
    </span>
  </div>
);
SentimentIndicator.defaultProps = {
  sentiment: 'NEUTRO',
};
SentimentIndicator.propTypes = {
  sentiment: PropTypes.oneOf(['POSITIVO', 'NEGATIVO', 'NEUTRO', 'MIX']),
};
