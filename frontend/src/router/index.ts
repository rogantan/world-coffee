import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw, Router } from 'vue-router';
import LoginLayout from '../components/layouts/LoginLayout.vue';
import MainLayout from '../components/layouts/MainLayout.vue';
import HomePage from '../components/HomePage.vue';

const loginRoutes: RouteRecordRaw[] = [
    {
        path: '/signin',
        component: LoginLayout,
        children: [
            {
                path: '',
                component: () => import("../views/auth/AuthorizationView.vue"),
            },
        ],
    }
]

const mainRoutes: RouteRecordRaw[] = [
    {
        path: '/main',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                component: HomePage,
                meta: {
                    name: "Главная страница"
                }
            }
        ]
    }
]

const settingsRoutes: RouteRecordRaw[] = [
    {
        path: '/settings',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'synch',
                component: () => import("../components/settings/Synchronization.vue"),
                meta: {
                    name: "Проверка синхронизации"
                }
            },
            {
                path: 'users',
                component: () => import("../components/settings/UserAccess.vue"),
                meta: {
                    name: "Пользователи"
                }
            }
        ]
    }
]

const listsRoutes: RouteRecordRaw[] = [
    {
        path: "/lists",
        component: MainLayout,
        children: [
            {
                path: "retail_stores",
                component: () => import("../components/lists/RetailStores.vue"),
                meta: {
                    name: "Точки продаж"
                }
            },
            {
                path: "payment_purposes",
                component: () => import("../components/lists/PaymentPurpose.vue"),
                meta: {
                    name: "Назначения платежа"
                }
            },
            {
                path: "bonuses",
                component: () => import("../components/lists/Bonuses.vue"),
                meta: {
                    name: "Премии"
                }
            }
        ]
    }
]

const testRoutes: RouteRecordRaw[] = [
    {
        path: "/tests",
        component: MainLayout,
        children: [
            {
                path: '',
                component: () => import("../components/tests/TestsPage.vue"),
                meta: {
                    name: "Тестирования"
                }
            },
            {
                path: 'result',
                component: () => import("../components/tests/TestResult.vue"),
                meta: {
                    name: "Результаты тестирований"
                }
            },
            {
                path: 'create',
                component: () => import("../components/tests/admin/TestCreatePage.vue"),
                meta: {
                    name: "Добавление тестирования"
                }
            },
            {
                name: 'TestEdit',
                path: 'edit',
                component: () => import('../components/tests/admin/TestEditPage.vue'),
                meta: {
                    name: 'Редактирование теста'
                }
            },
            {
                name: 'TestStarted',
                path: 'started',
                component: () => import('../components/tests/TestStartedPage.vue'),
                meta: {
                    name: 'Тестирование'
                }
            },
            {
                name: 'TestsShowResult',
                path: 'result-show',
                component: () => import("../components/tests/TestShowResultPage.vue"),
                meta: {
                    name: "Результаты теста"
                }
            }
        ]
    }
]

const reportRoutes: RouteRecordRaw[] = [
    {
        path: '/reports',
        component: MainLayout,
        children: [
            {
                path: 'auditor',
                component: () =>  import("../components/reports/Auditor.vue"),
                meta: {
                    name: "Ревизор"
                }
            },
            {
                path: 'sales-journal',
                component: () => import("../components/reports/SalesJournal.vue"),
                meta: {
                    name: "Журнал продаж"
                }
            },
            {
                path: 'payment-journal',
                component: () => import("../components/reports/PaymentJournal.vue"),
                meta: {
                    name: "Журнал платежей"
                }
            },
            {
                path: "revenue-month",
                component: () => import("../components/reports/RevenueMonthPage.vue"),
                meta: {
                    name: "Выручка в месяц"
                }
            },
            {
                path: "shift-day",
                component: () => import("../components/reports/ShiftDayPage.vue"),
                meta: {
                    name: "Подсчёт смен (день)"
                }
            },
            {
                path: 'shift-month',
                component: () => import("../components/reports/ShiftMonthPage.vue"),
                meta: {
                    name: "Подсчёт смен (месяц)"
                }
            }
        ]
    }
]

const dashboardRoutes: RouteRecordRaw[] = [
    {
        path: '/dashboard',
        component: MainLayout,
        children: [
            {
                path: "1",
                component: () => import("../components/reports/DashboardPage.vue"),
                meta: {
                    name: "Coffee Point",
                    back_url: "Coffee Point"
                }
            },
            {
                path: "2",
                component: () => import("../components/reports/DashboardPage.vue"),
                meta: {
                    name: "Coffee Enjoy",
                    back_url: "Coffee Enjoy"
                }
            }
        ]
    }
]

const errorRoutes: RouteRecordRaw[] = [
    {
        path: '/error',
        component: MainLayout,
        children: [
            {
                path: 'access_denied',
                component: () => import("../components/errors/AccessDenied.vue"),
            },
            {
                path: 'not_found',
                component: () => import("../components/errors/PageNotFound.vue"),
            }
        ]
    }
]

const inventoryRoutes: RouteRecordRaw[] = [
    {
        path: '/inventory',
        component: MainLayout,
        children: [
            {
                path: "1",
                component: () => import("../components/inventory/InventoryPage.vue"),
                meta: {
                    name: "Инвентаризация Coffee Point",
                    back_url: "Coffee Point"
                }
            },
            {
                path: "2",
                component: () => import("../components/inventory/InventoryPage.vue"),
                meta: {
                    name: "Инвентаризация Coffee Enjoy",
                    back_url: "Coffee Enjoy"
                }
            }
        ]
    }
]

const router: Router = createRouter({
    history: createWebHistory(''),
    routes: [
        {
            path: "/",
            redirect: "/signin",
        },
        ...loginRoutes,
        ...mainRoutes,
        ...listsRoutes,
        ...reportRoutes,
        ...settingsRoutes,
        ...errorRoutes,
        ...testRoutes,
        ...dashboardRoutes,
        ...inventoryRoutes
    ]
});
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token')

    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
        return next('/signin')
    }

    next()
})
export default router;