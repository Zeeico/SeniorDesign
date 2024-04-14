/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.h
 * @brief          : Header for main.c file.
 *                   This file contains the common defines of the application.
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2024 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */
extern ADC_HandleTypeDef hadc1;
extern DMA_HandleTypeDef hdma_adc1;

extern CAN_HandleTypeDef hcan;

extern I2C_HandleTypeDef hi2c1;
extern I2C_HandleTypeDef hi2c2;

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define ALARM_Output_Pin GPIO_PIN_13
#define ALARM_Output_GPIO_Port GPIOC
#define thermistorIn0_Pin GPIO_PIN_0
#define thermistorIn0_GPIO_Port GPIOA
#define controller0exti_Pin GPIO_PIN_1
#define controller0exti_GPIO_Port GPIOA
#define controller0exti_EXTI_IRQn EXTI1_IRQn
#define thermistorIn1_Pin GPIO_PIN_3
#define thermistorIn1_GPIO_Port GPIOA
#define controller1exti_Pin GPIO_PIN_4
#define controller1exti_GPIO_Port GPIOA
#define controller1exti_EXTI_IRQn EXTI4_IRQn
#define controller2exti_Pin GPIO_PIN_6
#define controller2exti_GPIO_Port GPIOA
#define controller2exti_EXTI_IRQn EXTI9_5_IRQn
#define thermisorIn2_Pin GPIO_PIN_7
#define thermisorIn2_GPIO_Port GPIOA
#define thermistorIn3_Pin GPIO_PIN_1
#define thermistorIn3_GPIO_Port GPIOB
#define controller3exti_Pin GPIO_PIN_2
#define controller3exti_GPIO_Port GPIOB
#define controller3exti_EXTI_IRQn EXTI2_IRQn
#define relay3cmd_Pin GPIO_PIN_12
#define relay3cmd_GPIO_Port GPIOB
#define relay2cmd_Pin GPIO_PIN_13
#define relay2cmd_GPIO_Port GPIOB
#define relay1cmd_Pin GPIO_PIN_14
#define relay1cmd_GPIO_Port GPIOB
#define relay0cmd_Pin GPIO_PIN_15
#define relay0cmd_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
