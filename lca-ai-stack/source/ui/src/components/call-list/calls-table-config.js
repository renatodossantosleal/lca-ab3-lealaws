// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import React from 'react';

import Button from '@cloudscape-design/components/button';
import ButtonDropdown from '@cloudscape-design/components/button-dropdown';
import CollectionPreferences from '@cloudscape-design/components/collection-preferences';
import Icon from '@cloudscape-design/components/icon';
import Link from '@cloudscape-design/components/link';
import SpaceBetween from '@cloudscape-design/components/space-between';
import StatusIndicator from '@cloudscape-design/components/status-indicator';
import Popover from '@cloudscape-design/components/popover';

import rehypeRaw from 'rehype-raw';
import ReactMarkdown from 'react-markdown';
import { TableHeader } from '../common/table';
import { CALLS_PATH } from '../../routes/constants';
import { SentimentIndicator } from '../sentiment-icon/SentimentIcon';
import { SentimentTrendIndicator } from '../sentiment-trend-icon/SentimentTrendIcon';
import { CategoryAlertPill } from './CategoryAlertPill';
import { CategoryPills } from './CategoryPills';
import { getTextOnlySummary } from '../common/summary';

export const KEY_COLUMN_ID = 'callId';

export const COLUMN_DEFINITIONS_MAIN = [
  {
    id: KEY_COLUMN_ID,
    header: 'ID',
    cell: (item) => <Link href={`#${CALLS_PATH}/${item.callId}`}>{item.callId}</Link>,
    sortingField: 'callId',
    width: 200,
  },
  {
    id: 'alerts',
    header: '⚠',
    cell: (item) => (
      <CategoryAlertPill alertCount={item.alertCount} categories={item.callCategories} />
    ),
    sortingField: 'alertCount',
    width: 85,
  },
  {
    id: 'agentId',
    header: 'Agente',
    cell: (item) => item.agentId,
    sortingField: 'agentId',
  },
  {
    id: 'initiationTimeStamp',
    header: 'Hora de Início',
    cell: (item) => item.initiationTimeStamp,
    sortingField: 'initiationTimeStamp',
    isDescending: false,
    width: 225,
  },
  {
    id: 'summary',
    header: 'Resumo',
    cell: (item) => {
      const summary = getTextOnlySummary(item.callSummaryText);
      return (
        <Popover
          dismissButton={false}
          position="top"
          size="large"
          triggerType="text"
          content={<ReactMarkdown rehypePlugins={[rehypeRaw]}>{summary ?? ''}</ReactMarkdown>}
        >
          {summary && summary.length > 20 ? `${summary.substring(0, 20)}...` : summary}
        </Popover>
      );
    },
    sortingField: 'summary',
  },
  {
    id: 'callerPhoneNumber',
    header: 'Tel. Cliente',
    cell: (item) => item.callerPhoneNumber,
    sortingField: 'callerPhoneNumber',
    width: 175,
  },
  {
    id: 'recordingStatus',
    header: 'Status',
    cell: (item) => (
      <StatusIndicator type={item.recordingStatusIcon}>
        {` ${item.recordingStatusLabel} `}
      </StatusIndicator>
    ),
    sortingField: 'recordingStatusLabel',
    width: 150,
  },
  {
    id: 'callerSentiment',
    header: 'Sentimento Cliente',
    cell: (item) => <SentimentIndicator sentiment={item?.callerSentimentLabel} />,
    sortingField: 'callerSentimentLabel',
  },
  {
    id: 'callerSentimentTrend',
    header: 'Sentimento Cliente Trend',
    cell: (item) => <SentimentTrendIndicator trend={item?.callerSentimentTrendLabel} />,
    sortingField: 'callerSentimentTrendLabel',
  },
  {
    id: 'agentSentiment',
    header: 'Sentimento Agente',
    cell: (item) => <SentimentIndicator sentiment={item?.agentSentimentLabel} />,
    sortingField: 'agentSentimentLabel',
  },
  {
    id: 'agentSentimentTrend',
    header: 'Sentimento Agente Trend',
    cell: (item) => <SentimentTrendIndicator trend={item?.agentSentimentTrendLabel} />,
    sortingField: 'agentSentimentTrendLabel',
  },
  {
    id: 'conversationDuration',
    header: 'Duração',
    cell: (item) => item.conversationDurationTimeStamp,
    sortingField: 'conversationDurationTimeStamp',
  },
  {
    id: 'menu',
    header: '',
    cell: (item) => (
      <ButtonDropdown
        items={[
          {
            text: 'Open in PCA',
            href: item.pcaUrl,
            external: true,
            disabled: !item.pcaUrl,
            externalIconAriaLabel: '(opens in new tab)',
          },
        ]}
        expandToViewport
      >
        <Icon name="menu" />
      </ButtonDropdown>
    ),
    width: 120,
  },
  {
    id: 'callCategories',
    header: 'Categorias',
    cell: (item) => <CategoryPills categories={item.callCategories} />,
    sortingField: 'callCategoryCount',
    width: 200,
  },
];

export const DEFAULT_SORT_COLUMN = COLUMN_DEFINITIONS_MAIN[3];

export const SELECTION_LABELS = {
  itemSelectionLabel: (data, row) => `select ${row.callId}`,
  allItemsSelectionLabel: () => 'select all',
  selectionGroupLabel: 'Call selection',
};

const PAGE_SIZE_OPTIONS = [
  { value: 10, label: '10 Chamadas' },
  { value: 30, label: '30 Chamadas' },
  { value: 50, label: '50 Chamadas' },
];

const VISIBLE_CONTENT_OPTIONS = [
  {
    label: 'Call list properties',
    options: [
      { id: 'callId', label: 'Call ID', editable: false },
      { id: 'alerts', label: 'Alertas' },
      { id: 'agentId', label: 'Agente' },
      { id: 'initiationTimeStamp', label: 'Hora de Início' },
      { id: 'callerPhoneNumber', label: 'Tel. Cliente' },
      { id: 'recordingStatus', label: 'Status' },
      { id: 'summary', label: 'Resumo' },
      { id: 'callerSentiment', label: 'Sentimento Cliente' },
      { id: 'callerSentimentTrend', label: 'Sentimento Cliente Trend' },
      { id: 'agentSentiment', label: 'Sentimento Agente' },
      { id: 'agentSentimentTrend', label: 'Sentimento Agente Trend' },
      { id: 'conversationDuration', label: 'Duração' },
      { id: 'menu', label: 'Menu' },
      { id: 'callCategories', label: 'Categorias' },
    ],
  },
];

const VISIBLE_CONTENT = [
  'alerts',
  'agentId',
  'initiationTimeStamp',
  'callerPhoneNumber',
  'recordingStatus',
  'summary',
  'callerSentiment',
  'callerSentimentTrend',
  'conversationDuration',
  'menu',
];

export const DEFAULT_PREFERENCES = {
  pageSize: PAGE_SIZE_OPTIONS[0].value,
  visibleContent: VISIBLE_CONTENT,
  wraplines: false,
};

/* eslint-disable react/prop-types, react/jsx-props-no-spreading */
export const CallsPreferences = ({
  preferences,
  setPreferences,
  disabled,
  pageSizeOptions = PAGE_SIZE_OPTIONS,
  visibleContentOptions = VISIBLE_CONTENT_OPTIONS,
}) => (
  <CollectionPreferences
    title="Preferences"
    confirmLabel="Confirmar"
    cancelLabel="Cancelar"
    disabled={disabled}
    preferences={preferences}
    onConfirm={({ detail }) => setPreferences(detail)}
    pageSizePreference={{
      title: 'Quantidade de Chamadas',
      options: pageSizeOptions,
    }}
    // wrapLinesPreference={{
    //   label: 'Wrap lines',
    //   description: 'Check to see all the text and wrap the lines',
    // }}
    visibleContentPreference={{
      title: 'Selecione as colunas visíveis',
      options: visibleContentOptions,
    }}
  />
);

// number of shards per day used by the list calls API
export const CALL_LIST_SHARDS_PER_DAY = 6;
const TIME_PERIOD_DROPDOWN_CONFIG = {
  'refresh-2h': { count: 0.5, text: '2 hrs' },
  'refresh-4h': { count: 1, text: '4 hrs' },
  'refresh-8h': { count: CALL_LIST_SHARDS_PER_DAY / 3, text: '8 hrs' },
  'refresh-1d': { count: CALL_LIST_SHARDS_PER_DAY, text: '1 dia' },
  'refresh-2d': { count: 2 * CALL_LIST_SHARDS_PER_DAY, text: '2 dias' },
  'refresh-1w': { count: 7 * CALL_LIST_SHARDS_PER_DAY, text: '1 semana' },
  'refresh-2w': { count: 14 * CALL_LIST_SHARDS_PER_DAY, text: '2 semanas' },
  'refresh-1m': { count: 30 * CALL_LIST_SHARDS_PER_DAY, text: '30 dias' },
};
const TIME_PERIOD_DROPDOWN_ITEMS = Object.keys(TIME_PERIOD_DROPDOWN_CONFIG).map((k) => ({
  id: k,
  ...TIME_PERIOD_DROPDOWN_CONFIG[k],
}));

// local storage key to persist the last periods to load
export const PERIODS_TO_LOAD_STORAGE_KEY = 'periodsToLoad';

export const CallsCommonHeader = ({ resourceName = 'Calls', ...props }) => {
  const onPeriodToLoadChange = ({ detail }) => {
    const { id } = detail;
    const shardCount = TIME_PERIOD_DROPDOWN_CONFIG[id].count;
    props.setPeriodsToLoad(shardCount);
    localStorage.setItem(PERIODS_TO_LOAD_STORAGE_KEY, JSON.stringify(shardCount));
  };

  // eslint-disable-next-line
  const periodText =
    TIME_PERIOD_DROPDOWN_ITEMS.filter((i) => i.count === props.periodsToLoad)[0]?.text || '';

  return (
    <TableHeader
      title={resourceName}
      actionButtons={
        <SpaceBetween size="xxs" direction="horizontal">
          <ButtonDropdown
            loading={props.loading}
            onItemClick={onPeriodToLoadChange}
            items={TIME_PERIOD_DROPDOWN_ITEMS}
          >
            {`Período: ${periodText}`}
          </ButtonDropdown>
          <Button
            iconName="refresh"
            variant="normal"
            loading={props.loading}
            onClick={() => props.setIsLoading(true)}
          />
          <Button
            iconName="download"
            variant="normal"
            loading={props.loading}
            onClick={() => props.downloadToExcel()}
          />
        </SpaceBetween>
      }
      {...props}
    />
  );
};
