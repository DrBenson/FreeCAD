/***************************************************************************
 *   Copyright (c) 2022 WandererFan <wandererfan@gmail.com>                *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/

#include "PreCompiled.h"

#include <App/DocumentObject.h>
#include <App/Link.h>
#include <Mod/TechDraw/App/DrawPage.h>
#include <Mod/TechDraw/App/DrawProjGroupItem.h>
#include <Mod/TechDraw/App/DrawTemplate.h>

#include "ViewProviderPageExtension.h"
#include "ViewProviderPage.h"


using namespace TechDrawGui;

EXTENSION_PROPERTY_SOURCE(TechDrawGui::ViewProviderPageExtension, Gui::ViewProviderExtension)

ViewProviderPageExtension::ViewProviderPageExtension()
{
    initExtensionType(ViewProviderPageExtension::getExtensionClassTypeId());
}

ViewProviderPageExtension::~ViewProviderPageExtension() {}

bool ViewProviderPageExtension::extensionCanDragObjects() const { return true; }

//we don't want another extension to drag our objects, so we say that we can handle this object
bool ViewProviderPageExtension::extensionCanDragObject(App::DocumentObject* docObj) const
{
    (void)docObj;
    return true;
}

//we don't take any action on drags.  everything is handling in drop
void ViewProviderPageExtension::extensionDragObject(App::DocumentObject* obj) { (void)obj; }

//we handle our own drops
bool ViewProviderPageExtension::extensionCanDropObjects() const { return true; }

bool ViewProviderPageExtension::extensionCanDropObject(App::DocumentObject* obj) const
{
    // Accept links to views as well.
    if (obj->isDerivedFrom<App::Link>()) {
        auto* link = static_cast<App::Link*>(obj);
        obj = link->getLinkedObject();
    }

    //only DrawView objects can live on pages (except special case Template)
    if (obj->isDerivedFrom<TechDraw::DrawView>()) {
        return true;
    }
    if (obj->isDerivedFrom<TechDraw::DrawTemplate>()) {
        //don't let another extension try to drop templates
        return true;
    }

    return false;
}

bool ViewProviderPageExtension::extensionCanDropObjectEx(App::DocumentObject* obj, App::DocumentObject* owner,
    const char* subname,
    const std::vector<std::string>& elements) const
{
    Q_UNUSED(owner);
    Q_UNUSED(subname);
    Q_UNUSED(elements);

    // Accept links to views as well.
    if (obj->isDerivedFrom<App::Link>()) {
        auto* link = static_cast<App::Link*>(obj);
        obj = link->getLinkedObject();
    }

    //only DrawView objects can live on pages (except special case Template)
    if (obj->isDerivedFrom<TechDraw::DrawView>()) {
        return true;
    }
    if (obj->isDerivedFrom<TechDraw::DrawTemplate>()) {
        //don't let another extension try to drop templates
        return true;
    }

    return false;
}

void ViewProviderPageExtension::extensionDropObject(App::DocumentObject* obj)
{
    bool linkToView = false;
    if (obj->isDerivedFrom<App::Link>()) {
        auto* link = static_cast<App::Link*>(obj);
        if (link->getLinkedObject()->isDerivedFrom<TechDraw::DrawView>()) {
            linkToView = true;
        }
    }

    if (obj->isDerivedFrom<TechDraw::DrawView>() || linkToView) {
        dropObject(obj);
        return;
    }
}

//this code used to live in ViewProviderPage
void ViewProviderPageExtension::dropObject(App::DocumentObject* obj)
{
    if (obj->isDerivedFrom<TechDraw::DrawProjGroupItem>()) {
        //DPGI can not be dropped onto the Page if it belongs to DPG
        auto* dpgi = static_cast<TechDraw::DrawProjGroupItem*>(obj);
        if (dpgi->getPGroup()) {
            return;
        }
    }
    if (obj->isDerivedFrom<App::Link>()) {
        auto* link = static_cast<App::Link*>(obj);
        obj = link->getLinkedObject();
        if (!obj->isDerivedFrom<TechDraw::DrawView>()) {
            return;
        }

        std::vector<App::DocumentObject*> deps;
        for (auto& inObj : obj->getInList()) {
            if (inObj && inObj->isDerivedFrom<TechDraw::DrawView>()) {
                deps.push_back(inObj);
            }
        }

        TechDraw::DrawPage* page = nullptr;
        for (auto& inObj : link->getInList()) {
            if (inObj->isDerivedFrom<TechDraw::DrawPage>()) {
                page = static_cast<TechDraw::DrawPage*>(inObj);
            }
        }
        if (page) {
            for (auto* dep : deps) {
                page->removeView(dep);
            }
            page->removeView(link);
        }

        getViewProviderPage()->getDrawPage()->addView(link, false);
        for (auto* dep : deps) {
            getViewProviderPage()->getDrawPage()->addView(dep, false);
        }

        return;
    }

    if (obj->isDerivedFrom<TechDraw::DrawView>()) {
        auto dv = static_cast<TechDraw::DrawView*>(obj);

        std::vector<App::DocumentObject*> deps;
        for (auto* dep : dv->getInList()) {
            if (dep && dep->isDerivedFrom<TechDraw::DrawView>()) {
                deps.push_back(dep);
            }
        }

        auto* parentPage = dv->findParentPage();
        if (parentPage) {
            for (auto* dep : deps) {
                parentPage->removeView(dep);
            }
            parentPage->removeView(dv);
        }

        getViewProviderPage()->getDrawPage()->addView(dv, false);
        for (auto* dep : deps) {
            getViewProviderPage()->getDrawPage()->addView(dep, false);
        }

        //don't run ancestor's method as addView does everything we need
        return;
    }
    //don't try to drop random objects
}

const ViewProviderPage* ViewProviderPageExtension::getViewProviderPage() const
{
    return dynamic_cast<const ViewProviderPage*>(getExtendedViewProvider());
}


const char* ViewProviderPageExtension::whoAmI() const
{
    auto parent = getViewProviderPage();
    if (parent) {
        return parent->whoAmI();
    }
    return nullptr;
}

namespace Gui
{
EXTENSION_PROPERTY_SOURCE_TEMPLATE(TechDrawGui::ViewProviderPageExtensionPython,
                                   TechDrawGui::ViewProviderPageExtension)

// explicit template instantiation
template class TechDrawGuiExport
    ViewProviderExtensionPythonT<TechDrawGui::ViewProviderPageExtension>;
}// namespace Gui
