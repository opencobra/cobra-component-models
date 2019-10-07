# Copyright (c) 2019, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a mixin that tracks creation and update timestamps."""


from datetime import datetime, timezone

from sqlalchemy import Column, DateTime


def timezone_aware_now():
    """Return the date and time in this moment in the universal timezone."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """
    Define creation and update time columns to be mixed in with other tables.

    Attributes
    ----------
    created_on : datetime
        By default this value is populated at instantiation with the time of
        the moment.
    updated_on : datetime
        The time is automatically populated whenever the database model is
        updated.

    """

    created_on: datetime = Column(
        DateTime(timezone=True), nullable=False, default=timezone_aware_now
    )
    updated_on: datetime = Column(
        DateTime(timezone=True), nullable=True, onupdate=timezone_aware_now
    )
