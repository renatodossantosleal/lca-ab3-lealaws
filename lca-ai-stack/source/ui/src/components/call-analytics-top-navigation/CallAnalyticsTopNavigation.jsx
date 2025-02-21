// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import React, { useState } from 'react';
import Box from '@cloudscape-design/components/box';
import Button from '@cloudscape-design/components/button';
import Modal from '@cloudscape-design/components/modal';
import SpaceBetween from '@cloudscape-design/components/space-between';
import TopNavigation from '@cloudscape-design/components/top-navigation';
import { Auth, Logger } from 'aws-amplify';

import useAppContext from '../../contexts/app';

const logger = new Logger('TopNavigation');

/* eslint-disable react/prop-types */
const SignOutModal = ({ visible, setVisible }) => {
  async function signOut() {
    try {
      await Auth.signOut();
      logger.debug('signed out');
      window.location.reload();
    } catch (error) {
      logger.error('error signing out: ', error);
    }
  }
  return (
    <Modal
      onDismiss={() => setVisible(false)}
      visible={visible}
      closeAriaLabel="Close modal"
      size="medium"
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="link" onClick={() => setVisible(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={() => signOut()}>
              Sair
            </Button>
          </SpaceBetween>
        </Box>
      }
      header="Sair"
    >
      Sair da aplicação?
    </Modal>
  );
};

const CallAnalyticsTopNavigation = () => {
  const { user } = useAppContext();
  const userId = user?.attributes?.email || 'user';
  const [isSignOutModalVisible, setIsSignOutModalVisiblesetVisible] = useState(false);
  return (
    <>
      <div id="top-navigation" style={{ position: 'sticky', top: 0, zIndex: 1002 }}>
        <TopNavigation
          identity={{ href: '#', title: 'Módulo de Inteligência da Octank' }}
          i18nStrings={{ overflowMenuTriggerText: 'More' }}
          utilities={[
            {
              type: 'menu-dropdown',
              text: userId,
              description: userId,
              iconName: 'user-profile',
              items: [
                {
                  id: 'signout',
                  type: 'button',
                  text: (
                    <Button
                      variant="primary"
                      onClick={() => setIsSignOutModalVisiblesetVisible(true)}
                    >
                      Sair
                    </Button>
                  ),
                },
              ],
            },
          ]}
        />
      </div>
      <SignOutModal
        visible={isSignOutModalVisible}
        setVisible={setIsSignOutModalVisiblesetVisible}
      />
    </>
  );
};

export default CallAnalyticsTopNavigation;
